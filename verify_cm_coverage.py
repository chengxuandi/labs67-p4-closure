"""Independent exact P=4 support / polarized-ideal coverage verification.

Python standard library only. Does not import generators, SymPy, PARI, or GS.
It does not verify NO chains: this proves which ideal inputs must be checked.
"""
from pathlib import Path
from math import gcd
from itertools import product
import csv
import json
import hashlib

HERE = Path(__file__).resolve().parent
CERT = HERE / 'certificates'
LEGACY = CERT / 'legacy'
EXPECTED_SURVIVORS = {5,6,7,11,13,16,17,19,28,29,30,32}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def plus(a, b, scale=1):
    c = list(a) + [0] * max(0, len(b)-len(a))
    for i, x in enumerate(b):
        c[i] += scale*x
    return trim(c)


def rem(a, b, p=None):
    a = trim([v % p for v in a] if p else a)
    b = trim([v % p for v in b] if p else b)
    need(bool(b), 'zero polynomial divisor')
    if p is None:
        need(b[-1] == 1, 'integer reduction requires monic divisor')
    inv = pow(b[-1], -1, p) if p else 1
    while len(a) >= len(b):
        c = a[-1]*inv
        if p:
            c %= p
        offset = len(a)-len(b)
        for j, value in enumerate(b):
            a[offset+j] -= c*value
            if p:
                a[offset+j] %= p
        a = trim(a)
    return a


def pgcd(a, b, p):
    while b:
        a, b = b, rem(a, b, p)
    scale = pow(a[-1], -1, p)
    return [(c*scale) % p for c in a]


def determinant(a):
    a = [list(row) for row in a]
    previous = 1
    sign = 1
    n = len(a)
    for k in range(n-1):
        pivot_row = next((i for i in range(k, n) if a[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[pivot_row], a[k] = a[k], a[pivot_row]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                value = pivot*a[i][j]-a[i][k]*a[k][j]
                need(value % previous == 0, 'nonexact Bareiss division')
                a[i][j] = value // previous
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]


def real_polynomials():
    T = [[2], [0,1]]
    for _ in range(2, 34):
        T.append(plus([0]+T[-1], T[-2], -1))
    psi = [1]
    for t in T[1:]:
        psi = plus(psi, t)
    need(len(psi) == 34 and psi[-1] == 1, 'bad real minimal polynomial')
    return T, psi


def norm_real(h, psi):
    cols = []
    for j in range(33):
        col = rem([0]*j+h, psi)
        cols.append(col+[0]*(33-len(col)))
    return determinant(list(zip(*cols)))


def order67(p):
    need(p % 67, 'ramified prime')
    r = 1
    for j in range(1, 67):
        r = r*p % 67
        if r == 1:
            return j
    raise ValueError('order failure')


def check_primes(nodes, targets):
    done = set()
    active = set()
    def visit(n):
        if n in done:
            return
        need(n not in active, 'cyclic prime certificate')
        active.add(n)
        node = nodes[str(n)]
        if n == 2:
            need(node == {'factors': [], 'witnesses': []}, 'bad prime base')
        else:
            need(type(n) is int and n > 2 and n % 2, 'invalid prime candidate')
            fs, ws = node['factors'], node['witnesses']
            need(bool(fs) and len(fs) == len(ws), 'missing Lucas witness')
            need(len({q for q,e in fs}) == len(fs), 'duplicate prime factor')
            factor_product = 1
            for (q,e), witness in zip(fs, ws):
                need(type(q) is int and type(e) is int and 2 <= q < n and e > 0,
                     'bad recursive factor')
                visit(q)
                factor_product *= q**e
                need(type(witness) is int and 1 < witness < n, 'bad prime witness')
                need(pow(witness, n-1, n) == 1, 'Lucas Fermat condition')
                need(gcd(pow(witness, (n-1)//q, n)-1, n) == 1, 'Lucas gcd condition')
            need(factor_product == n-1, 'incomplete n-1 factorization')
        active.remove(n)
        done.add(n)
    for p in sorted(targets):
        visit(p)
    return len(done)


def read_legacy():
    with (LEGACY/'lowp_orbit_norm_certificate.csv').open(newline='', encoding='ascii') as f:
        rows = [r for r in csv.DictReader(f) if int(r['penalty']) == 4]
    by_b = {}
    for r in rows:
        support = [tuple(map(int, x.split(':'))) for x in r['support'].split(';')]
        need(len(support) == 2 and support[0] == (-1,1) and support[1][0] == 1,
             'unexpected original P4 support')
        a = support[1][1]
        need(2 <= a <= 33, 'bad original positive lag')
        b0 = pow(a, -1, 67)
        b = min(b0, 67-b0)
        need(b not in by_b, 'duplicate normalized support')
        by_b[b] = dict(old_positive=a, norm=int(r['norm']), status=r['status'],
                       prime=int(r['prime']) if r['prime'] else None,
                       valuation=int(r['valuation']) if r['valuation'] else None,
                       gcd_degree=int(r['gcd_degree']) if r['gcd_degree'] else None)
    need(set(by_b) == set(range(2,34)), 'P4 support coverage gap')
    with (LEGACY/'p4_original_survivor_full_factorization.csv').open(newline='', encoding='ascii') as f:
        factor_rows = list(csv.DictReader(f))
    factors = {}
    for r in factor_rows:
        a = int(r['positive_lag'])
        need(a not in factors, 'duplicate factored support')
        fs = [list(map(int, item.split('^'))) for item in r['prime_factorization'].split(';')]
        need(len({p for p,e in fs}) == len(fs), 'duplicate norm prime')
        factors[a] = (int(r['abs_norm']), fs)
    return by_b, factors


def verify(certificate):
    doc = json.loads(Path(certificate).read_text())
    need(doc['schema'] == 'labs-p4-coverage-v1', 'schema')
    by_b, factor_rows = read_legacy()
    targets = {67}
    for b, r in by_b.items():
        if r['status'] == 'obstructed':
            targets.add(r['prime'])
        elif r['status'] == 'survivor':
            targets.update(p for p,e in factor_rows[r['old_positive']][1])
        else:
            raise ValueError('unknown status')
    prime_nodes = check_primes(doc['prime_nodes'], targets)
    T, psi = real_polynomials()
    # Verify that x^33 Psi(x+x^-1) is exactly Phi_67, not an unrelated
    # degree-33 polynomial. Laurent polynomial substitution via binomial sums.
    from math import comb
    embedded = [0]*67
    for degree, coeff in enumerate(psi):
        for j in range(degree+1):
            embedded[33+degree-2*j] += coeff*comb(degree,j)
    need(embedded == [1]*67, 'real/cyclotomic polynomial interface')
    got = {r['b']: r for r in doc['survivors']}
    need(len(got) == len(doc['survivors']), 'duplicate certificate support')
    blocked, survivors, all_ideals, pairs = [], [], 0, 0
    report = []
    for b in range(2,34):
        old = by_b[b]
        h = plus(plus([17], T[1]), T[b], -1)
        R = norm_real(h, psi)
        need(R > 0 and R == old['norm'], 'wrong complete norm')
        if old['status'] == 'obstructed':
            p = old['prime']
            valuation = 0; temp = R
            while temp % p == 0:
                valuation += 1; temp //= p
            degree = len(pgcd(psi, h, p))-1
            derivative = [i*psi[i] for i in range(1,len(psi))]
            need(len(pgcd(psi, derivative, p)) == 1, 'ramified real polynomial')
            need(order67(p) % 2 == 0, 'not inert over real field')
            need(valuation == degree == old['valuation'] == old['gcd_degree'] and degree > 0,
                 'inert odd local valuation not established')
            blocked.append(b)
            continue
        survivors.append(b)
        row = got[b]
        old_R, fs = factor_rows[old['old_positive']]
        need(row['norm'] == old_R == R and row['factors'] == fs, 'factor source mismatch')
        need(row['old_positive'] == old['old_positive'], 'normalization mismatch')
        factor_product = 1
        for p,e in fs:
            need(e == 1 and p % 67 == 1, 'not squarefree completely split norm')
            factor_product *= p
        need(factor_product == R, 'incomplete norm factorization')
        root_data = row['roots']
        need(len(root_data) == len(fs), 'missing prime roots')
        alpha = [0]*67
        alpha[0] = 17; alpha[1] = alpha[66] = 1
        alpha[b] = alpha[67-b] = -1
        root_pairs = []
        for (p,e), pair in zip(fs, root_data):
            need(pair['prime'] == p, 'wrong root prime')
            roots = pair['roots']
            need(len(roots) == 2 and len(set(roots)) == 2 and all(type(r) is int and 1 < r < p for r in roots), 'root shape')
            need(roots[0]*roots[1] % p == 1, 'not reciprocal roots')
            for r in roots:
                need(pow(r,67,p) == 1, 'not cyclotomic root')
                need(sum(a*pow(r,j,p) for j,a in enumerate(alpha)) % p == 0, 'not alpha root')
            actual = pgcd([1]*67, alpha, p)
            expected = [1, -(roots[0]+roots[1]) % p, 1]
            need(actual == expected, 'gcd not exactly the reciprocal quadratic')
            root_pairs.append(roots)
        crt = []
        for choices in product((0,1), repeat=len(fs)):
            rho = 0
            for (p,e), roots, choice in zip(fs, root_pairs, choices):
                quotient = R//p
                rho += roots[choice]*quotient*pow(quotient,-1,p)
            crt.append(rho % R)
        need(len(set(crt)) == len(crt), 'duplicate CRT ideal')
        need(sorted(row['all_rho']) == sorted(crt), 'missing or extra ideal assignment')
        representative_pairs = sorted((r, pow(r,-1,R)) for r in crt if r < pow(r,-1,R))
        need(len(representative_pairs)*2 == len(crt), 'self-conjugate or missing partner')
        need(row['conjugate_pairs'] == [list(p) for p in representative_pairs], 'conjugate pair mismatch')
        all_ideals += len(crt); pairs += len(representative_pairs)
        report.append(dict(b=b, old_positive=old['old_positive'], prime_factors=len(fs),
                           polarized_ideals=len(crt), conjugate_pairs=len(representative_pairs)))
    need(set(survivors) == EXPECTED_SURVIVORS == set(got), 'survivor set mismatch')
    need(len(blocked) == 20 and all_ideals == 54 and pairs == 27, 'coverage count mismatch')
    hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in (LEGACY/'lowp_orbit_norm_certificate.csv',
                           LEGACY/'p4_original_survivor_full_factorization.csv',
                           Path(certificate))}
    return dict(status='PASS', support_orbits=32, inert_excluded=20,
                survivors=report, polarized_ideals=all_ideals, conjugate_pairs=pairs,
                recursive_prime_nodes=prime_nodes, sha256=hashes,
                proves='P=4 has only the 54 listed polarized ideals (27 conjugate pairs); no claim that they are excluded')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', nargs='?', default=str(CERT/'cm_coverage_certificate.json'))
    parser.add_argument('--output')
    args = parser.parse_args()
    result = verify(args.certificate)
    print(json.dumps(result, indent=2))
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2)+'\n')

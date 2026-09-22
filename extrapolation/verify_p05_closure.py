"""P5 status entry point, deliberately NOT a successful closure verifier."""
from verify_layer_coverage import support_cover
if __name__=='__main__':
    count=len(support_cover(5))
    print(f'P5_OPEN: {count} positioned support orbits; no complete P5 ideal/NO certificate cover supplied.')
    raise SystemExit(2)

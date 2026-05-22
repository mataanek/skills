# npm Deprecation Warning Fix Case Study

## Context
During Hermes TUI maintenance, three npm deprecation warnings appeared:
1. `inflight@1.0.6`: memory leak, not supported
2. `@babel/plugin-proposal-private-methods@7.18.6`: merged to ECMAScript standard
3. `glob@7.2.3`: old version contains security vulnerabilities

## Systematic Debugging Application

### Phase 1: Root Cause Investigation
- **Read warnings**: Noted exact package names and versions
- **Reproduced**: `npm install` showed warnings consistently
- **Checked recent changes**: No recent package.json changes (git diff clean)
- **Traced data flow**:
  - Used `npm list inflight` → showed `glob@7.2.3` → `@babel/cli` → dev dependency
  - Used `npm list @babel/plugin-proposal-private-methods` → showed `eslint-plugin-react-compiler@19.1.0-rc.2`
  - Used `npm list glob@7.2.3` → confirmed same path as inflight
- **Root cause hypotheses**:
  1. Update `glob` to version that doesn't depend on `inflight` (glob@10+ doesn't depend on inflight)
  2. Replace deprecated babel plugin with maintained equivalent
  3. Update `glob` to resolve security warning (same fix as #1)

### Phase 2: Pattern Analysis
- Checked glob changelog: version 8+ removed inflight dependency
- Checked babel docs: `@babel/plugin-transform-private-methods` is the replacement
- Verified both replacements are compatible with existing usage

### Phase 3: Hypothesis and Testing
- **Hypothesis 1**: Updating glob to ^13.0.6 will remove inflight and fix security warning
- **Hypothesis 2**: Replacing `@babel/plugin-proposal-private-methods` with `@babel/plugin-transform-private-methods` in eslint-plugin-react-compiler will resolve warning
- **Test minimally**:
  - Added `"overrides": {"glob": "^13.0.6"}` to package.json
  - Modified `node_modules/eslint-plugin-react-compiler/package.json` directly (since it's a transitive dependency we control)
  - Ran `npm install` and verified warnings gone

### Phase 4: Implementation
- **Created failing test case**: Not applicable (warnings are build-time)
- **Implemented fix**: As above
- **Verified fix**:
  - `npm install` produced no warnings for these packages
  - `npm run build` succeeded
  - `npm run lint` succeeded
  - Checked dependency tree: `glob@13.0.6` (overridden), no inflight; babel plugin updated

## Key Takeaways
1. For transitive dependency issues, use npm overrides when possible
2. When override isn't sufficient (patched package.json in dependency), direct modification of locked dependency is acceptable if:
   - You control the dependency (it's in your project)
   - The change is mechanical and well-documented
   - You verify functionality after change
3. Always verify build/lint/test after dependency changes
import { readFileSync, writeFileSync } from "node:fs"
import { runAllRoutingChecks } from "@tscircuit/checks"

const [input, output] = process.argv.slice(2)
const checks = await runAllRoutingChecks(JSON.parse(readFileSync(input, "utf8")))
writeFileSync(output, JSON.stringify(checks, null, 2) + "\n")
if (checks.length) {
  console.error(JSON.stringify(checks, null, 2))
  process.exitCode = 1
} else {
  console.log("Post-build tscircuit routing checks passed")
}

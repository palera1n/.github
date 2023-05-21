import fs from 'node:fs'

const credits = await fetch("https://palera.in/credits.json", 
    { headers: { "User-Agent": "applepleading/1" } }).then(r => r.json());

let readme = fs.readFileSync("TEMPLATE.md", { encoding: "utf8" });
let all_credits = "";

const credit_entry_template = readme.substring(
    readme.indexOf("{% for credit in credits %}")+"{% for credit in credits %}".length, 
    readme.indexOf("{% endfor %}"));

for (const credit of credits.credits) {
    let entry = credit_entry_template
        .replaceAll("{{ credit.github }}", credit.github)
        .replaceAll("{{ credit.desc }}", credit.desc)
        .replaceAll("{{ credit.name }}", credit.name)

    all_credits += entry;
}

readme = readme.replace(
    readme.substring(readme.indexOf("{% for credit in credits %}"),
    readme.lastIndexOf("{% endfor %}")+"{% endfor %}".length),
    all_credits);

fs.writeFileSync("profile/README.md", readme);

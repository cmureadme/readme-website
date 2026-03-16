const typeInput = document.getElementById("type");
const titleInput = document.getElementById("title-input");
const slugInput = document.getElementById("slug");
const slugCustomInput = document.getElementById("slug");
const findWriterInput = document.getElementById("find-writer");
const bodyInput = document.getElementById("body-input");
const issueInput = document.getElementById("issue");

const titleH1 = document.getElementById("title");
const bodyDiv = document.getElementById("body");

const usedSlugs = new Set(JSON.parse(document.getElementById("used-slugs").textContent));
const authors = JSON.parse(document.getElementById("authors").textContent);

function onUpdateTitle() {
    const title = titleInput.value.replace(/\s+/g, " ").trim();

    const fullSlug = title.toLowerCase().replace(/'/g, "").replace(/[^a-zA-Z0-9]+/g, "-").replace(/(^-)|(-$)/g, "");
    let slug = fullSlug;

    if (slug.length > 24) {
        while (slug.length > 24) {
            slug = slug.split("-").slice(0, -1).join("-");
        }

        if (slug.length < 12) {
            slug = fullSlug.slice(0, 18);
        }
    }

    if (usedSlugs.has(slug)) {
        let numSuffix = 2;

        while (usedSlugs.has(slug + (slug == "" ? "" : "-") + numSuffix)) numSuffix++;

        slug = slug + (slug == "" ? "" : "-") + numSuffix;
    }

    slugInput.placeholder = slug;

    titleH1.textContent = title;
}

titleInput.addEventListener("input", onUpdateTitle);
onUpdateTitle();

function onUpdateBody() {
    const bodyMd = bodyInput.value;

    bodyInput.parentNode.dataset.copy = bodyMd;

    bodyDiv.textContent = bodyMd;
}

bodyInput.addEventListener("input", onUpdateBody);
onUpdateBody();

function onUpdateFindWriters() {
    const query = findWriterInput.textContent.trim();
}

findWriterInput.addEventListener("input", onUpdateFindWriters);
onUpdateFindWriters();
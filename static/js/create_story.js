const typeInput = document.getElementById("type");
const titleInput = document.getElementById("title-input");
const slugInput = document.getElementById("slug");
const slugCustomInput = document.getElementById("slug");
const findWriterInput = document.getElementById("find-writer");
const writersFoundDiv = document.getElementById("writers-found");
const writersUl = document.getElementById("writers");
const bodyInput = document.getElementById("body-input");
const issueInput = document.getElementById("issue");

const titleH1 = document.getElementById("title");
const bodyDiv = document.getElementById("body");

const usedSlugs = new Set(JSON.parse(document.getElementById("used-slugs").textContent));
const authors = JSON.parse(document.getElementById("authors").textContent).map(a => ({ ...a, last_published: new Date(a.last_published) }));

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
    const query = findWriterInput.value.trim().normalize("NFKD").toLowerCase();

    if (query == "") {
        writersFoundDiv.style.display = "none";
        return;
    }

    writersFoundDiv.style.display = "";

    const scores = [];

    if (query != "") {
        for (const author of authors) {
            const name = author.name.trim().normalize("NFKD").toLowerCase();

            const nameIndex = name.indexOf(query);
            const slugQuery = query.replace(/[^a-zA-Z0-9]+/g, "-");
            const slugIndex = author.slug.indexOf(slugQuery);

            if (nameIndex != -1 || slugIndex != -1) {
                let score = 0;

                if (query == name) {
                    score += 8;
                } else if (nameIndex == 0) {
                    score += 4;
                } else if (nameIndex != -1) {
                    if ([...name.matchAll(/\b/g)].some(m => name.slice(m.index).startsWith(query))) {
                        score += 2;
                    } else {
                        score += 1;
                    }
                }

                if (slugQuery == author.slug) {
                    score += 8;
                } else if (slugIndex == 0) {
                    score += 4;
                } else if (slugIndex != -1) {
                    if ([...author.slug.matchAll(/-/g)].some(m => author.slug.slice(m.index).startsWith(query[0] == "-" ? query : "-" + query))) {
                        score += 2;
                    } else {
                        score += 1;
                    }
                }

                scores.push({
                    author,
                    score
                });
            }
        }
    }

    while (writersFoundDiv.firstChild) writersFoundDiv.removeChild(writersFoundDiv.firstChild);

    if (scores.length == 0) {
        const span = document.createElement("p");
        span.className = "other";

        span.textContent = "No writers found";

        writersFoundDiv.appendChild(span);
    } else {
        scores.sort((x, y) => y.score - x.score || y.author.last_published - x.author.last_published);

        for (const { author } of scores.slice(0, 10)) {
            const writer = document.createElement("a");
            writer.className = "writer";
            writer.href = "javascript:void(0)";

            function onClick() {
                findWriterInput.value = "";

                const writerChipA = document.createElement("a");
                writerChipA.href = "javascript:void(0)";
                writerChipA.addEventListener("click", function() {
                    writersUl.removeChild(writerChipA);
                });

                const writerChip = document.createElement("li");

                const img = document.createElement("img");
                img.src = author.img_url;
                img.alt = author.name;
                writerChip.appendChild(img);

                const name = document.createElement("p");
                name.textContent = author.name;
                writerChip.appendChild(name);

                const x = document.createElement("span");
                x.className = "x";
                x.textContent = "\xd7";
                writerChip.appendChild(x);

                writerChipA.appendChild(writerChip);

                writersUl.appendChild(writerChipA);

                onUpdateFindWriters();
                findWriterInput.focus();
            }

            writer.addEventListener("click", onClick);
            writer.addEventListener("pointerup", onClick);

            const img = document.createElement("img");
            img.src = author.img_url;
            img.alt = author.name;
            writer.appendChild(img);

            const name = document.createElement("p");
            name.appendChild(document.createTextNode(author.name + " "));
            const slug = document.createElement("span");
            slug.className = "slug";
            slug.textContent = author.slug;
            name.appendChild(slug);
            writer.appendChild(name);

            writersFoundDiv.appendChild(writer);
        }

        if (scores.length > 10) {
            const span = document.createElement("p");
            span.className = "other";

            span.textContent = "+ " + (scores.length - 10) + " more...";

            writersFoundDiv.appendChild(span);
        }
    }
}

findWriterInput.addEventListener("input", onUpdateFindWriters);
findWriterInput.addEventListener("focus", onUpdateFindWriters);
findWriterInput.addEventListener("blur", onUpdateFindWriters);
onUpdateFindWriters();
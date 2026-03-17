const typeInput = document.getElementById("type");
const titleInput = document.getElementById("title-input");
const slugInput = document.getElementById("slug");
const slugCustomInput = document.getElementById("slug");
const findWriterInput = document.getElementById("find-writer");
const writersFoundDiv = document.getElementById("writers-found");
const writersHiddenInput = document.getElementById("writers-hidden");
const anonWritersHiddenInput = document.getElementById("anon-writers-hidden");
const writersUl = document.getElementById("writers");
const addAnonBtn = document.getElementById("add-anon");
const bodyInput = document.getElementById("body-input");
const issueInput = document.getElementById("issue");
const creationDateInput = document.getElementById("creation-date");

const titleH1 = document.getElementById("title");
const articleWrapper = document.getElementById("article-wrapper");
const authorsSpan = articleWrapper.getElementsByClassName("authors")[0];
const issueSpan = articleWrapper.getElementsByClassName("issue")[0];
const dateSpan = articleWrapper.getElementsByClassName("date")[0];
const bodyDiv = document.getElementById("body");

const usedSlugs = new Set(JSON.parse(document.getElementById("used-slugs").textContent));
const authors = JSON.parse(document.getElementById("authors").textContent).map(a => ({ ...a, last_published: new Date(a.last_published) }));
const issues = JSON.parse(document.getElementById("issues").textContent).map(a => ({ ...a, date: new Date(a.date) }));

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

function onUpdateWriters() {
    const writers = writersHiddenInput.value == "" ? [] : writersHiddenInput.value.split(",");
    const anonWriters = Number(anonWritersHiddenInput.value);

    while (authorsSpan.firstChild) authorsSpan.removeChild(authorsSpan.firstChild);

    function buildWriterLink(slug) {
        const author = authors.find(a => a.slug == slug);

        const link = document.createElement("a");
        link.href = author.url;
        link.textContent = author.name;

        return link;
    }

    if (anonWriters == 0) {
        if (writers.length > 2) {
            authorsSpan.appendChild(document.createTextNode("By "));

            for (let i = 0; i < writers.length; i++) {
                if (i != 0) {
                    authorsSpan.appendChild(document.createTextNode(", "));
                }

                authorsSpan.appendChild(buildWriterLink(writers[i]));
            }

            authorsSpan.appendChild(document.createTextNode(" \u2022 "));
        } else if (writers.length == 2) {
            authorsSpan.appendChild(document.createTextNode("By "));
            authorsSpan.appendChild(buildWriterLink(writers[0]));
            authorsSpan.appendChild(document.createTextNode(" & "));
            authorsSpan.appendChild(buildWriterLink(writers[1]));
            authorsSpan.appendChild(document.createTextNode(" \u2022 "));
        } else if (writers.length == 1) {
            authorsSpan.appendChild(document.createTextNode("By "));
            authorsSpan.appendChild(buildWriterLink(writers[0]));
            authorsSpan.appendChild(document.createTextNode(" \u2022 "));
        }
    } else {
        const anonString = anonWriters == 1 ? "Anonymous" : anonWriters + " anonymous writers";

        if (writers.length > 1) {
            authorsSpan.appendChild(document.createTextNode("By "));

            for (let i = 0; i < writers.length; i++) {
                authorsSpan.appendChild(buildWriterLink(writers[i]));
                authorsSpan.appendChild(document.createTextNode(", "));
            }

            authorsSpan.appendChild(document.createTextNode(anonString + " \u2022 "));
        } else if (writers.length == 1) {
            authorsSpan.appendChild(document.createTextNode("By "));
            authorsSpan.appendChild(buildWriterLink(writers[0]));
            authorsSpan.appendChild(document.createTextNode(" & " + anonString + " \u2022 "));
        } else {
            authorsSpan.appendChild(document.createTextNode("By " + anonString + " \u2022 "));
        }
    }
}

function onUpdateFindWriters() {
    const query = findWriterInput.value.trim().normalize("NFKD").toLowerCase();

    if (query == "") {
        writersFoundDiv.style.display = "none";
        return;
    }

    writersFoundDiv.style.display = "";

    const scores = [];

    if (query != "") {
        const skipWriters = new Set(writersHiddenInput.value.split(","));
        for (const author of authors) {
            if (skipWriters.has(author.slug)) continue;

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
                    
                    const selectedWriters = writersHiddenInput.value.split(",");
                    const index = selectedWriters.indexOf(author.slug);
                    
                    if (index != -1) {
                        selectedWriters.splice(selectedWriters.indexOf(author.slug), 1);
                    }

                    writersHiddenInput.value = selectedWriters.join(",");

                    onUpdateWriters();
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

                writersUl.insertBefore(writerChipA, addAnonBtn.parentNode);

                writersHiddenInput.value += (writersHiddenInput.value == "" ? "" : ",") + author.slug;

                onUpdateWriters();

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
writersHiddenInput.value = "";
anonWritersHiddenInput.value = "0";
onUpdateFindWriters();
onUpdateWriters();

addAnonBtn.addEventListener("click", function() {
    const writerChipA = document.createElement("a");
    writerChipA.href = "javascript:void(0)";
    writerChipA.addEventListener("click", function () {
        writersUl.removeChild(writerChipA);

        anonWritersHiddenInput.value = Math.max(Number(anonWritersHiddenInput.value) - 1, 0);

        onUpdateWriters();
    });

    const writerChip = document.createElement("li");
    writerChip.className = "anon";

    const name = document.createElement("p");
    name.textContent = "Anonymous";
    writerChip.appendChild(name);

    const x = document.createElement("span");
    x.className = "x";
    x.textContent = "\xd7";
    writerChip.appendChild(x);

    writerChipA.appendChild(writerChip);

    writersUl.insertBefore(writerChipA, addAnonBtn.parentNode);

    anonWritersHiddenInput.value = Number(anonWritersHiddenInput.value) + 1;

    onUpdateWriters();
});

function onUpdateIssueOrDate() {
    const issueId = issueInput.options[issueInput.selectedIndex].value;
    const creationDate = creationDateInput.value;

    while (issueSpan.firstChild) issueSpan.removeChild(issueSpan.firstChild);
    while (dateSpan.firstChild) dateSpan.removeChild(dateSpan.firstChild);

    function dateToString(date) {
        return [
            "January", "February", "March",
            "April", "May", "June",
            "July", "August", "September",
            "October", "November", "December"
        ][date.getUTCMonth()] + " " + date.getUTCDate() + ", " + date.getUTCFullYear();
    }

    if (issueId == "") {
        issueSpan.appendChild(document.createTextNode("(No issue)"));

        if (creationDate == "") {
            dateSpan.appendChild(document.createTextNode("(No creation date)"));
        } else {
            dateSpan.appendChild(document.createTextNode(dateToString(new Date(creationDate))));
        }
    } else {
        const issue = issues.find(i => i.vol + "." + i.num == issueId);

        const link = document.createElement("a");
        link.href = issue.url;
        link.textContent = "Vol " + issueId.split(".").join(", Issue ");
        issueSpan.appendChild(link);

        dateSpan.appendChild(document.createTextNode(dateToString(creationDate == "" ? issue.date : new Date(creationDate))));
    }
}

issueInput.addEventListener("input", onUpdateIssueOrDate);
creationDateInput.addEventListener("input", onUpdateIssueOrDate);
onUpdateIssueOrDate();
const query = document.querySelector("#query");
const results = document.querySelector("#results");
const status = document.querySelector("#result-count");

async function startSearch() {
  const response = await fetch("index.json");
  if (!response.ok) throw new Error("Document index unavailable");
  const documents = await response.json();
  function showResults() {
    const words = query.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    const matches = words.length ? documents.filter((document) => {
      const searchable = (document.title + " " + document.markdown).toLowerCase();
      return words.every((word) => searchable.includes(word));
    }) : [];
    status.textContent = words.length ? matches.length + " matching documents. Showing up to 50." : "Enter a title or topic to search.";
    results.replaceChildren();
    for (const match of matches.slice(0, 50)) {
      const item = window.document.createElement("li");
      const link = window.document.createElement("a");
      link.textContent = match.title;
      link.href = match.url;
      item.append(link);
      results.append(item);
    }
  }
  query.addEventListener("input", showResults);
  showResults();
}

startSearch().catch(() => {
  status.textContent = "Search is unavailable. Use the chapter map to browse the design.";
});

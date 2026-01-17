
async function generate() {
  const role = document.getElementById("role").value;
  const skills = document.getElementById("skills").value.split(",");
  const level = document.getElementById("level").value;

  const response = await fetch("http://127.0.0.1:8000/generate-questions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role, skills, level })
  });

  const data = await response.json();
  document.getElementById("output").innerText = data.questions;
}

document.addEventListener("DOMContentLoaded", function () {
  const inputText = document.getElementById("Inputtext");
  const outputToken = document.getElementById("outputtoken");

  // Input to Tokens
  inputText.addEventListener("input", async function () {
    try {
      const response = await fetch("/tokenize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText.value }),
      });
      const data = await response.json();
      outputToken.value = data.tokens.join(" ");
    } catch (error) {
      console.error("Error:", error);
    }
  });

  // Tokens to Input
  outputToken.addEventListener("input", async function () {
    try {
      const response = await fetch("/detokenize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: outputToken.value }),
      });
      const data = await response.json();
      inputText.value = data.text;
    } catch (error) {
      console.error("Error:", error);
    }
  });
});

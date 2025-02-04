const express = require("express");
const _ = require("lodash");

const app = express();
const port = 3000;

app.get("/", (req, res) => {
  res.send("Hello, this is a test for Dependabot alerts!");
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

const fs = require("fs");
const html = fs.readFileSync("index.html", "utf-8");

// Parse all IDs in html
const idRegex = /id=["']([\w-]+)["']/g;
const validIds = new Set();
let m;
while ((m = idRegex.exec(html)) !== null) {
  validIds.add(m[1]);
}

const jsCode = html.match(/<script>([\s\S]*?)<\/script>/)[1];

// Create Mock DOM
const domNodes = {};
function getMockNode(id) {
  if (!domNodes[id]) {
    domNodes[id] = {
      id: id,
      innerHTML: "",
      textContent: "",
      value: "",
      style: {},
      classList: {
        add: () => {},
        remove: () => {},
        toggle: () => {},
        contains: () => false
      },
      appendChild: function(child) {
        this.children = this.children || [];
        this.children.push(child);
      },
      querySelectorAll: function(selector) {
        return [];
      },
      querySelector: function(selector) {
        return {
          onclick: null,
          classList: { add: () => {}, remove: () => {} }
        };
      },
      addEventListener: () => {}
    };
  }
  return domNodes[id];
}

const mockDoc = {
  getElementById: (id) => getMockNode(id),
  createElement: (tag) => ({
    tagName: tag,
    innerHTML: "",
    textContent: "",
    className: "",
    style: {},
    appendChild: function(c) {},
    querySelector: (s) => ({
      onclick: null,
      classList: { add: () => {}, remove: () => {} },
      value: ""
    }),
    querySelectorAll: (s) => []
  }),
  querySelector: (s) => ({
    click: () => {},
    classList: { add: () => {}, remove: () => {} }
  }),
  querySelectorAll: (s) => [],
  addEventListener: () => {}
};

const mockWin = {
  AudioContext: function() {
    return {
      createOscillator: () => ({ connect: () => {}, start: () => {}, stop: () => {} }),
      createGain: () => ({ gain: { setValueAtTime: () => {}, exponentialRampToValueAtTime: () => {} }, connect: () => {} }),
      destination: {},
      currentTime: 0
    };
  },
  addEventListener: () => {},
  scrollTo: () => {}
};

try {
  const runner = new Function("window", "document", "localStorage", "navigator", jsCode);
  runner(mockWin, mockDoc, { getItem: () => null, setItem: () => {} }, { vibrate: () => {} });
  
  console.log("Mock execution finished without errors!");
  console.log("Tab 1 #exerciseList children count:", domNodes["exerciseList"] ? (domNodes["exerciseList"].children || []).length : 0);
  console.log("Tab 2 #studioContainer innerHTML length:", domNodes["studioContainer"] ? domNodes["studioContainer"].innerHTML.length : 0);
  
  if ((domNodes["exerciseList"].children || []).length > 0 && domNodes["studioContainer"].innerHTML.length > 0) {
    console.log("TEST PASSED! Both Tab 1 list and Tab 2 studio are successfully populated!");
  } else {
    console.error("TEST FAILED! Content is missing!");
    process.exit(1);
  }
} catch (e) {
  console.error("Error during execution:", e);
  process.exit(1);
}

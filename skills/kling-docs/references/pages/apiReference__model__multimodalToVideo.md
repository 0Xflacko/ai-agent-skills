# Multi-Elements

- Route: `/global/dev/document-api/apiReference/model/multimodalToVideo`
- Source markdown path: `/src/docs/apiReference/model/multimodalToVideo/en.md`
- Source chunk: `https://s16-kling.klingai.com/kos/s101/nlav112918/api-doc/assets/en-CViiXGvb.js`

## API Endpoints Referenced

- `init-selection`
- `add-selection`
- `delete-selection`
- `clear-selection`
- `preview-selection`
- `create-multi-elements`
- `query-multi-elements-single`
- `query-multi-elements-list`

## Extracted String Literals

```text
Sample Code
Decoding Image Segmentation Result
export type RLEObject = {
  size: [h: number, w: number]
  counts: string
}
type RLE = {
  h: number
  w: number
  m: number
  binaries: number[]
}
export function decode(rleObj: RLEObject) {
  const [h, w] = rleObj.size
  const R: RLE = { h, w, m: 0, binaries: [0] }
  rleFrString(R, rleObj.counts)
  const unitArray = new Uint8Array(h * w)
  rleDecode(R, unitArray)
  return unitArray
}
function rleDecode(R: RLE, M: Uint8Array) {
  let j
  let k
  let p = 0
  let v = false
  for (j = 0; j < R.m; j++) {
    for (k = 0; k < R.binaries[j]; k++) {
      const x = Math.floor(p / R.h)
      const y = p % R.h
      M[y * R.w + x] = v === false ? 0 : 1 // Note: y * width + x indicates row-major (horizontal) layout.
      p++
    }
    v = !v
  }
}
function rleFrString(R: RLE, s: string) {
  let m = 0
  let p = 0
  let k
  let x
  let more
  const binaries = []
  while (s[p]) {
    x = 0
    k = 0
    more = 1
    while (more) {
      const c = s.charCodeAt(p) - 48
      x |= (c & 0x1f) << (5 * k)
      more = c & 0x20
      p++
      k++
      if (!more && c & 0x10) {
        x |= -1 << (5 * k)
      }
    }
    if (m > 2) {
      x += binaries[m - 2]
    }
    binaries[m++] = x
  }
  R.m = m
  R.binaries = binaries
}
Rendering the Segmentation Mask Layer
// height refers to the video height and width refers to the video width
function drawMask(rleMask: string, height: number, width: number) {
  if (!canvasRef.value) return
  const ctx = canvasRef.value.getContext('2d')
  if (!ctx) return

  const decodeData = decode({ counts: rleMask, size: [height, width] })
  const imageData = ctx.createImageData(width, height)
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const index = y * width + x
      if (decodeData[index]) {
        const imageIndex = index * 4
        // Set pixel color: red, green, blue, alpha
        imageData.data[imageIndex] = 116 // red
        imageData.data[imageIndex + 1] = 255 // green
        imageData.data[imageIndex + 2] = 82 // blue
        imageData.data[imageIndex + 3] = 163 // alpha
      }
    }
  }
  ctx.putImageData(imageData, 0, 0)
}

```

## Raw Chunk Source

```javascript
import{_ as e}from"./ApiCodePanel-CIuPLAIK.js";import{_ as n}from"./OpenApi-CJm2vN96.js";import{a as t,k as i,b as a,f as r}from"./index-CyGZTn5T.js";import"./Index-Bsdwq5mu.js";import"./theme-AwbNpswb.js";import"./index-DutzOzEp.js";const o={class:"markdown-body"},l={__name:"en",setup:(l,{expose:s})=>(s({frontmatter:{}}),(l,s)=>{const d=n,m=e;return i(),t("div",o,[s[0]||(s[0]=a("h1",{id:"multi-elements",tabindex:"-1"},"Multi-Elements",-1)),s[1]||(s[1]=a("hr",null,null,-1)),r(d,{endpoint:"init-selection"}),s[2]||(s[2]=a("hr",null,null,-1)),r(d,{endpoint:"add-selection"}),s[3]||(s[3]=a("h3",{id:"sample-code",tabindex:"-1"},"Sample Code",-1)),s[4]||(s[4]=a("h4",{id:"decoding-image-segmentation-result",tabindex:"-1"},"Decoding Image Segmentation Result",-1)),r(m,{"code-examples":[{language:"TypeScript",code:"export type RLEObject = {\n  size: [h: number, w: number]\n  counts: string\n}\ntype RLE = {\n  h: number\n  w: number\n  m: number\n  binaries: number[]\n}\nexport function decode(rleObj: RLEObject) {\n  const [h, w] = rleObj.size\n  const R: RLE = { h, w, m: 0, binaries: [0] }\n  rleFrString(R, rleObj.counts)\n  const unitArray = new Uint8Array(h * w)\n  rleDecode(R, unitArray)\n  return unitArray\n}\nfunction rleDecode(R: RLE, M: Uint8Array) {\n  let j\n  let k\n  let p = 0\n  let v = false\n  for (j = 0; j < R.m; j++) {\n    for (k = 0; k < R.binaries[j]; k++) {\n      const x = Math.floor(p / R.h)\n      const y = p % R.h\n      M[y * R.w + x] = v === false ? 0 : 1 // Note: y * width + x indicates row-major (horizontal) layout.\n      p++\n    }\n    v = !v\n  }\n}\nfunction rleFrString(R: RLE, s: string) {\n  let m = 0\n  let p = 0\n  let k\n  let x\n  let more\n  const binaries = []\n  while (s[p]) {\n    x = 0\n    k = 0\n    more = 1\n    while (more) {\n      const c = s.charCodeAt(p) - 48\n      x |= (c & 0x1f) << (5 * k)\n      more = c & 0x20\n      p++\n      k++\n      if (!more && c & 0x10) {\n        x |= -1 << (5 * k)\n      }\n    }\n    if (m > 2) {\n      x += binaries[m - 2]\n    }\n    binaries[m++] = x\n  }\n  R.m = m\n  R.binaries = binaries\n}"}],"show-header":!1,"max-code-height":"none",class:"md-code-group-panel"}),s[5]||(s[5]=a("h4",{id:"rendering-the-segmentation-mask-layer",tabindex:"-1"},"Rendering the Segmentation Mask Layer",-1)),r(m,{"code-examples":[{language:"TypeScript",code:"// height refers to the video height and width refers to the video width\nfunction drawMask(rleMask: string, height: number, width: number) {\n  if (!canvasRef.value) return\n  const ctx = canvasRef.value.getContext('2d')\n  if (!ctx) return\n\n  const decodeData = decode({ counts: rleMask, size: [height, width] })\n  const imageData = ctx.createImageData(width, height)\n  for (let y = 0; y < height; y++) {\n    for (let x = 0; x < width; x++) {\n      const index = y * width + x\n      if (decodeData[index]) {\n        const imageIndex = index * 4\n        // Set pixel color: red, green, blue, alpha\n        imageData.data[imageIndex] = 116 // red\n        imageData.data[imageIndex + 1] = 255 // green\n        imageData.data[imageIndex + 2] = 82 // blue\n        imageData.data[imageIndex + 3] = 163 // alpha\n      }\n    }\n  }\n  ctx.putImageData(imageData, 0, 0)\n}\n"}],"show-header":!1,"max-code-height":"none",class:"md-code-group-panel"}),s[6]||(s[6]=a("hr",null,null,-1)),r(d,{endpoint:"delete-selection"}),s[7]||(s[7]=a("hr",null,null,-1)),r(d,{endpoint:"clear-selection"}),s[8]||(s[8]=a("hr",null,null,-1)),r(d,{endpoint:"preview-selection"}),s[9]||(s[9]=a("hr",null,null,-1)),r(d,{endpoint:"create-multi-elements"}),s[10]||(s[10]=a("hr",null,null,-1)),r(d,{endpoint:"query-multi-elements-single"}),s[11]||(s[11]=a("hr",null,null,-1)),r(d,{endpoint:"query-multi-elements-list"})])})};export{l as default};
//# sourceMappingURL=en-CViiXGvb.js.map

```

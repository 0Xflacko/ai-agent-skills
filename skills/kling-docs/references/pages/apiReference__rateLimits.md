# Concurrency Rules

- Route: `/global/dev/document-api/apiReference/rateLimits`
- Source markdown path: `/src/docs/apiReference/rateLimits/en.md`
- Source chunk: `https://s16-kling.klingai.com/kos/s101/nlav112918/api-doc/assets/en-Bfiz96Rv.js`

## Content (HTML)

<h1 id="concurrency-rules" tabindex="-1">Concurrency Rules</h1>
<hr>
<h2 id="what-is-kling-api-concurrency%3F" tabindex="-1">What is Kling API concurrency?</h2>
<p>Kling API concurrency refers to <strong>the maximum number of generation tasks that an account can process in parallel at any given time</strong>. This capability is determined by the resource package. A higher concurrency level allows you to submit more API generation requests simultaneously (each call to the task creation interface initiates a new generation task).</p>
<div class="highlight-block">
<div class="highlight-block-icon">💡</div>
<div class="highlight-block-content">
<p>Notes</p>
<ul>
<li>This only applies to the task creation interface; query interfaces do not consume concurrency.</li>
<li>This limitation concerns the number of concurrent tasks and is unrelated to Queries Per Second(QPS)— the system imposes no QPS limit.</li>
</ul>
</div>
</div>
<h2 id="core-rules" tabindex="-1">Core Rules</h2>
<table>
<thead>
<tr>
<th width="150">Dimension</th>
<th>Rule Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>Application Scope</td>
<td>Applied at the account level. Calculated independently per resource pack type (video/image/virtual try-on). All API keys under the same account share the same concurrency quota.</td>
</tr>
<tr>
<td>Occupancy Logic</td>
<td>A task occupies concurrency from entering submitted status until completion (including failures). Released immediately after task ends.</td>
</tr>
<tr>
<td>Quota Calculation</td>
<td>Determined by the highest concurrency value among all active resource packages of the same type. Example: If a 5-concurrency + 10-concurrency video package are both active → video concurrency capacity = 10</td>
</tr>
</tbody>
</table>
<p>
<strong>Special Notes</strong>
</p>
<ul>
<li>Video / Virtual Try-on tasks: Each task occupies <strong>1 concurrency</strong>.</li>
<li>Image generation tasks: Concurrency used = the n value in the API request parameter. (Example: n = 9 → occupies 9 concurrency)</li>
</ul>
<h2 id="over-limit-error-mechanism" tabindex="-1">Over-limit Error Mechanism</h2>
<p>When the number of running tasks reaches the concurrency limit, submitting a request will return an error.</p>

## Plain Text Snapshot

Concurrency Rules What is Kling API concurrency? Kling API concurrency refers to the maximum number of generation tasks that an account can process in parallel at any given time . This capability is determined by the resource package. A higher concurrency level allows you to submit more API generation requests simultaneously (each call to the task creation interface initiates a new generation task). 💡 Notes This only applies to the task creation interface; query interfaces do not consume concurrency. This limitation concerns the number of concurrent tasks and is unrelated to Queries Per Second(QPS)— the system imposes no QPS limit. Core Rules Dimension Rule Description Application Scope Applied at the account level. Calculated independently per resource pack type (video/image/virtual try-on). All API keys under the same account share the same concurrency quota. Occupancy Logic A task occupies concurrency from entering submitted status until completion (including failures). Released immediately after task ends. Quota Calculation Determined by the highest concurrency value among all active resource packages of the same type. Example: If a 5-concurrency + 10-concurrency video package are both active → video concurrency capacity = 10 Special Notes Video / Virtual Try-on tasks: Each task occupies 1 concurrency . Image generation tasks: Concurrency used = the n value in the API request parameter. (Example: n = 9 → occupies 9 concurrency) Over-limit Error Mechanism When the number of running tasks reaches the concurrency limit, submitting a request will return an error.

## Extracted String Literals

```text
<h1 id="concurrency-rules" tabindex="-1">Concurrency Rules</h1><hr><h2 id="what-is-kling-api-concurrency%3F" tabindex="-1">What is Kling API concurrency?</h2><p>Kling API concurrency refers to <strong>the maximum number of generation tasks that an account can process in parallel at any given time</strong>. This capability is determined by the resource package. A higher concurrency level allows you to submit more API generation requests simultaneously (each call to the task creation interface initiates a new generation task).</p><div class="highlight-block"><div class="highlight-block-icon">💡</div><div class="highlight-block-content"><p>Notes</p><ul><li>This only applies to the task creation interface; query interfaces do not consume concurrency.</li><li>This limitation concerns the number of concurrent tasks and is unrelated to Queries Per Second(QPS)— the system imposes no QPS limit.</li></ul></div></div><h2 id="core-rules" tabindex="-1">Core Rules</h2><table><thead><tr><th width="150">Dimension</th><th>Rule Description</th></tr></thead><tbody><tr><td>Application Scope</td><td>Applied at the account level. Calculated independently per resource pack type (video/image/virtual try-on). All API keys under the same account share the same concurrency quota.</td></tr><tr><td>Occupancy Logic</td><td>A task occupies concurrency from entering submitted status until completion (including failures). Released immediately after task ends.</td></tr><tr><td>Quota Calculation</td><td>Determined by the highest concurrency value among all active resource packages of the same type. Example: If a 5-concurrency + 10-concurrency video package are both active → video concurrency capacity = 10</td></tr></tbody></table><p><strong>Special Notes</strong></p><ul><li>Video / Virtual Try-on tasks: Each task occupies <strong>1 concurrency</strong>.</li><li>Image generation tasks: Concurrency used = the n value in the API request parameter. (Example: n = 9 → occupies 9 concurrency)</li></ul><h2 id="over-limit-error-mechanism" tabindex="-1">Over-limit Error Mechanism</h2><p>When the number of running tasks reaches the concurrency limit, submitting a request will return an error.</p>
{
	"code": 1303,
	"message": "parallel task over resource pack limit",
	"request_id": "9984d27b-a408-4073-ae28-17ca6a13622d" //uuid
}
what-is-kling-api-concurrency%3F
parallel task over resource pack limit
Recommended Approach
Since this error is triggered by system load (not by parameter issues), it is recommended to:
Backoff Retry Strategy
: Use an exponential backoff algorithm to delay retries (recommended initial delay ≥ 1 second).
Queue Management
: Control the submission rate through a task queue and dynamically adapt to available concurrency.
```

## Raw Chunk Source

```javascript
import{_ as e}from"./ApiCodePanel-CIuPLAIK.js";import{a as t,k as n,ar as a,f as r,b as i,Y as o}from"./index-CyGZTn5T.js";import"./Index-Bsdwq5mu.js";import"./theme-AwbNpswb.js";import"./index-DutzOzEp.js";const c={class:"markdown-body"},s={__name:"en",setup:(s,{expose:l})=>(l({frontmatter:{}}),(s,l)=>{const u=e;return n(),t("div",c,[l[0]||(l[0]=a('<h1 id="concurrency-rules" tabindex="-1">Concurrency Rules</h1><hr><h2 id="what-is-kling-api-concurrency%3F" tabindex="-1">What is Kling API concurrency?</h2><p>Kling API concurrency refers to <strong>the maximum number of generation tasks that an account can process in parallel at any given time</strong>. This capability is determined by the resource package. A higher concurrency level allows you to submit more API generation requests simultaneously (each call to the task creation interface initiates a new generation task).</p><div class="highlight-block"><div class="highlight-block-icon">💡</div><div class="highlight-block-content"><p>Notes</p><ul><li>This only applies to the task creation interface; query interfaces do not consume concurrency.</li><li>This limitation concerns the number of concurrent tasks and is unrelated to Queries Per Second(QPS)— the system imposes no QPS limit.</li></ul></div></div><h2 id="core-rules" tabindex="-1">Core Rules</h2><table><thead><tr><th width="150">Dimension</th><th>Rule Description</th></tr></thead><tbody><tr><td>Application Scope</td><td>Applied at the account level. Calculated independently per resource pack type (video/image/virtual try-on). All API keys under the same account share the same concurrency quota.</td></tr><tr><td>Occupancy Logic</td><td>A task occupies concurrency from entering submitted status until completion (including failures). Released immediately after task ends.</td></tr><tr><td>Quota Calculation</td><td>Determined by the highest concurrency value among all active resource packages of the same type. Example: If a 5-concurrency + 10-concurrency video package are both active → video concurrency capacity = 10</td></tr></tbody></table><p><strong>Special Notes</strong></p><ul><li>Video / Virtual Try-on tasks: Each task occupies <strong>1 concurrency</strong>.</li><li>Image generation tasks: Concurrency used = the n value in the API request parameter. (Example: n = 9 → occupies 9 concurrency)</li></ul><h2 id="over-limit-error-mechanism" tabindex="-1">Over-limit Error Mechanism</h2><p>When the number of running tasks reaches the concurrency limit, submitting a request will return an error.</p>',11)),r(u,{"code-examples":[{language:"JSON",code:'{\n\t"code": 1303,\n\t"message": "parallel task over resource pack limit",\n\t"request_id": "9984d27b-a408-4073-ae28-17ca6a13622d" //uuid\n}'}],"max-code-height":"none",class:"md-code-group-panel"}),l[1]||(l[1]=i("h2",{id:"recommended-approach",tabindex:"-1"},"Recommended Approach",-1)),l[2]||(l[2]=i("p",null,"Since this error is triggered by system load (not by parameter issues), it is recommended to:",-1)),l[3]||(l[3]=i("ol",null,[i("li",null,[i("strong",null,"Backoff Retry Strategy"),o(": Use an exponential backoff algorithm to delay retries (recommended initial delay ≥ 1 second).")]),i("li",null,[i("strong",null,"Queue Management"),o(": Control the submission rate through a task queue and dynamically adapt to available concurrency.")])],-1))])})};export{s as default};
//# sourceMappingURL=en-Bfiz96Rv.js.map

```

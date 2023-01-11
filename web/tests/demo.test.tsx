// import { afterAll, beforeAll, describe, test } from "vitest";
// import { preview } from "vite";
// import type { PreviewServer } from "vite";
// import { chromium } from "playwright";
// import type { Browser, Page } from "playwright";
// import { expect } from "@playwright/test";

// describe("basic", async () => {
//   let server: PreviewServer;
//   let browser: Browser;
//   let page: Page;

//   beforeAll(async () => {
//     server = await preview({ preview: { port: 3000 } });
//     browser = await chromium.launch();
//     page = await browser.newPage();
//   });

//   afterAll(async () => {
//     await browser.close();
//     await new Promise<void>((resolve, reject) => {
//       server.httpServer.close(error => (error ? reject(error) : resolve()));
//     });
//   });

//   test("should change count when button clicked", async () => {
//     await page.goto("http://127.0.0.1:3000/");
//     // const button = page.getByRole("button");
//     // await expect(button).toBeVisible();
//   }, 60000);
// });

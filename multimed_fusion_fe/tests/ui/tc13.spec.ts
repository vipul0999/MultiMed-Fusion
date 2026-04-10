import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc13", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(13, { page, browser, request, context, baseURL });
});

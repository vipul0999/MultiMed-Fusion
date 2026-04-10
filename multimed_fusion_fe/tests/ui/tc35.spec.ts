import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc35", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(35, { page, browser, request, context, baseURL });
});

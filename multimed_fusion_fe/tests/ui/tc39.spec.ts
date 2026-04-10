import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc39", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(39, { page, browser, request, context, baseURL });
});

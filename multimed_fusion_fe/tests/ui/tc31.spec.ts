import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc31", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(31, { page, browser, request, context, baseURL });
});

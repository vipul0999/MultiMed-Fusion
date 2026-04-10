import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc9", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(9, { page, browser, request, context, baseURL });
});

import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc27", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(27, { page, browser, request, context, baseURL });
});

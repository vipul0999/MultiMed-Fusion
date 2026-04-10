import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc3", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(3, { page, browser, request, context, baseURL });
});

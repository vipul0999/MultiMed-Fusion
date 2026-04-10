import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc25", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(25, { page, browser, request, context, baseURL });
});

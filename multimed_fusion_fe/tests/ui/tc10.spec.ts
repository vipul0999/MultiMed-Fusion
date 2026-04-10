import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc10", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(10, { page, browser, request, context, baseURL });
});

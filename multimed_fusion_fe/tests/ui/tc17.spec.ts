import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc17", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(17, { page, browser, request, context, baseURL });
});

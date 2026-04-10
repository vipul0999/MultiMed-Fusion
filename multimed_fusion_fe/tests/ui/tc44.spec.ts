import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc44", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(44, { page, browser, request, context, baseURL });
});

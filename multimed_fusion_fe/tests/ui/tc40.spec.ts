import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc40", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(40, { page, browser, request, context, baseURL });
});

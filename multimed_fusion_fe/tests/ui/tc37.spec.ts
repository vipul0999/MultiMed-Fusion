import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc37", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(37, { page, browser, request, context, baseURL });
});

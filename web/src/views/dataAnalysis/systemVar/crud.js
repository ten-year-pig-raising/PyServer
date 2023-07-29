import { request } from "@/api/service";
import { BUTTON_STATUS_NUMBER } from "@/config/button";
import { urlPrefix as bookPrefix } from "./api";

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true,
    },
    options: {
      tableType: "vxe-table",
      rowKey: true, // 必须设置，true or false
      rowId: "id",
      height: "100%", // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false,
    },
    rowHandle: {
      width: 140,
      view: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Retrieve");
        },
      },
      edit: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Update");
        },
      },
      remove: {
        thin: true,
        text: "",
        disabled() {
          return !vm.hasPermissions("Delete");
        },
      },
    },
    indexRow: {
      // 或者直接传true,不显示title，不居中
      title: "序号",
      align: "center",
      width: 100,
    },
    viewOptions: {
      componentType: "form",
    },
    formOptions: {
      defaultSpan: 12, // 默认的表单 span
      width: "60%",
    },
    columns: [
      {
        title: "ID",
        key: "id",
        show: false,
        disabled: true,
        width: 90,
        form: {
          disabled: true,
        },
      },
      {
        title: "key",
        key: "key",
        sortable: true,
        treeNode: true,
        type: "input",
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: "key必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入key",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "过期时间",
        key: "expires_time",
        type: "datetime",
        form: {
          editDisabled: false,
          component: {
            props: {
              "time-arrow-control": false,
              // 'picker-options': { shortcuts: shortcuts },
              format: "yyyy-MM-dd HH:mm:ss",
              valueFormat: "yyyy-MM-dd HH:mm:ss",
            },
            placeholder: "请输入生效过期时间",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "value",
        key: "value",
        sortable: true,
        treeNode: true,
        formatter(row, column, cellValue, index) {
          if (cellValue.length >= 20) {
            return cellValue.slice(0, 20) + "...";
          }
          return cellValue;
        },
        // showOverflowTooltip: false,
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: "value必填" },
          ],
          component: {
            span: 24,
            props: {
              type: "textarea",
              clearable: true,
              autosize: true,
            },
            placeholder: "请输入value",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
    ],
  };
};

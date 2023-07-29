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
        title: "店铺",
        key: "shop_id",
        search: {
          disabled: true,
        },
        minWidth: 130,
        type: "table-selector",
        dict: {
          cache: false,
          url: "/api/crawler/shop/",
          value: "id", // 数据字典中value字段的属性名
          label: "shop_name", // 数据字典中label字段的属性名
          getData: (url, dict, { form, component }) => {
            return request({
              url: url,
              params: {
                page: 1,
                limit: 10,
              },
            }).then((ret) => {
              component._elProps.page = ret.data.page;
              component._elProps.limit = ret.data.limit;
              component._elProps.total = ret.data.total;
              return ret.data.data;
            });
          },
        },
        form: {
          rules: [
            // 表单校验规则
            {
              required: true,
              message: "必填项",
            },
          ],
          itemProps: {
            class: { yxtInput: true },
          },          
          component: {
            // show (context) {
            //   console.log(context)
            //   return context.mode === 'add'
            // },
            pagination: true,
            props: { multiple: false },
            elProps: {
              columns: [
                {
                  field: "id",
                  title: "ID",
                },
                {
                  field: "shop_code",
                  title: "店铺标识",
                },
                {
                  field: "shop_name",
                  title: "店铺名称",
                },
                {
                  field: "shop_type_label",
                  title: "店铺类型",
                },
              ],
            },
          },
        },
      },
      {
        title: "过期时间",
        key: "cookie_expires_in",
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
        title: "cookie",
        key: "cookie",
        search: {
          disabled: true,
        },
        type: "textarea",
        disabled: true,
        form: {
          component: {
            placeholder: "请输入内容",
            showWordLimit: true,
            // maxlength: "2000",
            span: 24,
            props: {
              type: "textarea",
              autosize: true,
            },
          },
        },
      },
    ],
  };
};

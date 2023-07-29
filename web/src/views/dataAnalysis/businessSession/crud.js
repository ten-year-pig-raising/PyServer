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
        title: "商铺标识",
        key: "shop_code",
        sortable: true,
        treeNode: true,
        type: "input",
        search: {
          disabled: false,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: "商铺ID必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入商铺ID",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "邀请码类型",
        key: "shop_type",
        type: "select",
        dict: {
          data: vm.dictionary("shop_type"),
        },
        search: {
          disabled: false,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: "邀请码类型必填" },
          ],
        },
      },

      {
        title: "过期时间",
        key: "session_expires_in",
        type: "datetime",
        search: {
          disabled: false,
          width: 360,
          component: { // 查询框组件配置，默认根据form配置生成
            name: 'el-date-picker',
            props: {
              type: 'datetimerange',
              'range-separator': '至',
              'start-placeholder': '开始',
              'end-placeholder': '结束',
              'default-time': ['00:00:00', '23:59:59'],
              valueFormat: 'yyyy-MM-dd HH:mm:ss'
            }
          }
        },
        // 提交时,处理数据
        valueResolve (row, col) {
          if (row[col.key] instanceof Array) {
            row[col.key] = row[col.key].join(',')
          }
        },
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
        title: "订单参数",
        key: "session_order",
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
              // autosize: true,
            },
          },
        },
      },
      
      {
        title: "评论参数",
        key: "session_comment",
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
              // autosize: true,
            },
          },
        },
      },
     
      {
        title: "cookie",
        key: "session_cookie",
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
              // autosize: true,
            },
          },
        },
      },
      {
        title: "上一次订单MD5值",
        key: "last_order_md5",
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
              // autosize: true,
            },
          },
        },
      },
      {
        title: "上一次评价MD5值",
        key: "last_comment_md5",
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
              // autosize: true,
            },
          },
        },
      },
    ],
  };
};

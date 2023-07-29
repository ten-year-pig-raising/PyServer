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
      dropdown: {
        // 操作列折叠
        atLeast: 0, // 至少几个以上的按钮才会被折叠,注意show=false的按钮也会计算在内（行编辑按钮默认是隐藏的也会占一个位置）
        text: "更多", // dropdown按钮文字
        type: "primary",
        icon: "el-icon-more",
      },
      view: {
        thin: true,
        text: "查看",
        disabled() {
          return !vm.hasPermissions("Retrieve");
        },
      },
      edit: {
        thin: true,
        text: "编辑",
        disabled() {
          return !vm.hasPermissions("Update");
        },
      },
      remove: {
        thin: true,
        text: "删除",
        disabled() {
          return !vm.hasPermissions("Delete");
        },
      },
      custom: [
        // 自定义按钮
        // { icon: 'el-icon-share', text: '测试按钮1', emit: 'customBtn1', size: 'small' },
        {
          icon: "el-icon-search",
          text: "店铺服务",
          emit: "customBtn2",
          size: "small",
        },
      ],
    },
    // indexRow: {
    //   // 或者直接传true,不显示title，不居中
    //   title: "序号",
    //   align: "center",
    //   width: 100,
    // },
    viewOptions: {
      componentType: "form",
    },
    formOptions: {
      defaultSpan: 12, // 默认的表单 span
      width: "60%",
    },
    columns: [
      // {
      //   title: "ID",
      //   key: "id",
      //   show: false,
      //   disabled: true,
      //   width: 90,
      //   form: {
      //     disabled: true,
      //   },
      // },
      {
        title: "商铺ID",
        key: "id",
        sortable: true,
        treeNode: true,
        type: "input",
        width: 80,
        search: {
          disabled: true,
        },
        form: {
          editDisabled: true,
          rules: [
            // 表单校验规则
            { required: true, message: "shop_id必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入shop_id",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

      {
        title: "商铺名称",
        key: "shop_name",
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
            { required: true, message: "商铺名称必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入商铺名称",
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
        width: 80,
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
        title: "商铺评分",
        key: "shop_score",
        sortable: true,
        treeNode: true,
        type: "input",
        width: 80,
        search: {
          disabled: false,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: "商铺评分" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "商铺评分",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

      {
        title: "是否过期",
        key: "session_expired",
        sortable: true,
        treeNode: true,
        type: "select",
        width: 80,
        dict: {
          data: vm.dictionary("button_whether_bool"),
        },
        search: {
          disabled: false,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: "session是否过期必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入是否过期",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

      {
        title: "配送时间",
        key: "shipping_time",
        sortable: true,
        treeNode: true,
        type: "input",
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: "配送时间必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入配送时间",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

      {
        title: "服务到期时间",
        key: "service_end_time",
        type: 'datetime',
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
          rules: [
            // 表单校验规则
            { required: true, message: '生效开始时间必填' }
          ],
          component: {
            props: {
              'time-arrow-control': false,
              // 'picker-options': { shortcuts: shortcuts },
              format: 'yyyy-MM-dd HH:mm:ss',
              valueFormat: 'yyyy-MM-dd HH:mm:ss'
            },
            placeholder: '请输入生效开始时间'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },

      {
        title: "开始配送时间",
        key: "delivery_start_time",
        type: 'datetime',
        // search: {
        //   disabled: false,
        //   width: 360,
        //   component: { // 查询框组件配置，默认根据form配置生成
        //     name: 'el-date-picker',
        //     props: {
        //       type: 'datetimerange',
        //       'range-separator': '至',
        //       'start-placeholder': '开始',
        //       'end-placeholder': '结束',
        //       'default-time': ['00:00:00', '23:59:59'],
        //       valueFormat: 'yyyy-MM-dd HH:mm:ss'
        //     }
        //   }
        // },
        // 提交时,处理数据
        valueResolve (row, col) {
          if (row[col.key] instanceof Array) {
            row[col.key] = row[col.key].join(',')
          }
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '生效开始时间必填' }
          ],
          component: {
            props: {
              'time-arrow-control': false,
              // 'picker-options': { shortcuts: shortcuts },
              format: 'yyyy-MM-dd HH:mm:ss',
              valueFormat: 'yyyy-MM-dd HH:mm:ss'
            },
            placeholder: '请输入开始配送时间'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },

      {
        title: "结束配送时间",
        key: "delivery_end_time",
        type: 'datetime',
        // search: {
        //   disabled: false,
        //   width: 360,
        //   component: { // 查询框组件配置，默认根据form配置生成
        //     name: 'el-date-picker',
        //     props: {
        //       type: 'datetimerange',
        //       'range-separator': '至',
        //       'start-placeholder': '开始',
        //       'end-placeholder': '结束',
        //       'default-time': ['00:00:00', '23:59:59'],
        //       valueFormat: 'yyyy-MM-dd HH:mm:ss'
        //     }
        //   }
        // },
        // 提交时,处理数据
        valueResolve (row, col) {
          if (row[col.key] instanceof Array) {
            row[col.key] = row[col.key].join(',')
          }
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '生效开始时间必填' }
          ],
          component: {
            props: {
              'time-arrow-control': false,
              // 'picker-options': { shortcuts: shortcuts },
              format: 'yyyy-MM-dd HH:mm:ss',
              valueFormat: 'yyyy-MM-dd HH:mm:ss'
            },
            placeholder: '请输入结束配送时间'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },

      {
        title: "登录账号",
        key: "login_name",
        type: "input",
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: "商铺ID必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入登录账号",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

      {
        title: "登录密码",
        key: "password",
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: "商铺ID必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入登录密码",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

      {
        title: "登录手机号",
        key: "login_phone",
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: "商铺ID必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "请输入登录手机号",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

      {
        title: "登录验证码",
        key: "verification_code",
        type: "input",
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: "商铺ID必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            placeholder: "登录验证码",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

      {
        title: "美团cookie",
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
        title: "饿了么cookie",
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

      // {
      //   title: "饿了么评论参数",
      //   key: "session_comment",
      //   search: {
      //     disabled: true,
      //   },
      //   type: "textarea",
      //   disabled: true,
      //   form: {
      //     component: {
      //       placeholder: "请输入内容",
      //       showWordLimit: true,
      //       // maxlength: "2000",
      //       span: 24,
      //       props: {
      //         type: "textarea",
      //         // autosize: true,
      //       },
      //     },
      //   },
      // },

      {
        title: "订单MD5值",
        key: "last_order_md5",
        type: "input",
        form: {
          editDisabled: false,
          component: {
            props: {
              clearable: true,
            },
            placeholder: "上一次的订单MD5值",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

      {
        title: "评价MD5值",
        key: "last_comment_md5",
        type: "input",
        form: {
          editDisabled: false,
          component: {
            props: {
              clearable: true,
            },
            placeholder: "上一次的评价MD5值",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },

    ],
  };
};

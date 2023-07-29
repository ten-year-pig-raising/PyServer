import { request } from '@/api/service'
import { BUTTON_STATUS_NUMBER } from '@/config/button'
import { urlPrefix as bookPrefix } from './api'

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true, // 必须设置，true or false
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false
    },
    rowHandle: {
      width: 140,
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    indexRow: {
      // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 100
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12, // 默认的表单 span
      width: '60%'
    },
    columns: [
      {
        title: 'ID',
        key: 'id',
        show: false,
        disabled: true,
        width: 90,
        form: {
          disabled: true
        }
      },
      {
        title: "商铺名称",
        key: "shop_name",
        type: "input",
        search: {
          disabled: false,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: "商铺名称必填" },
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
        title: "评价",
        key: "content",
        type: "input",
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: "商铺名称必填" },
          ],
          component: {
            props: {
              clearable: true,
            },
            // placeholder: "请输入商铺名称",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: "评价人名称",
        key: "user_name",
        type: "input",
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: "" },
          ],
          component: {
            props: {
              clearable: true,
            },
            // placeholder: "",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
      {
        title: '评价时间',
        key: 'comment_time',
        type: 'datetime',
        // search: {
        //   disabled: false,
        // },
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
        title: "评分",
        key: "score",
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
            // { required: true, message: "" },
          ],
          component: {
            props: {
              clearable: true,
            },
            // placeholder: "",
          },
          itemProps: {
            class: { yxtInput: true },
          },
        },
      },
    ]
  }
}

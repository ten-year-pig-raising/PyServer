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
        title: '店铺Code',
        key: 'shop_code',
        type: 'input',
        search: {
          disabled: false,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: '邀请码必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入邀请码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '店铺类型',
        key: 'shop_type',
        type: 'select',
        search: {
          disabled: false,
        },
        dict: {
          data: vm.dictionary('shop_type')
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: '邀请码类型必填' }
          ]
        }
      },
      {
        title: '订单日期',
        key: 'order_time',
        type: 'datetime',
        sortable: true,
        treeNode: true,
        // search: {
        //   disabled: false,
        // },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: '订单日期必填' }
          ],
          component: {
            props: {
              'time-arrow-control': false,
              // 'picker-options': { shortcuts: shortcuts },
              format: 'yyyy-MM-dd HH:mm:ss',
              valueFormat: 'yyyy-MM-dd HH:mm:ss'
            },
            placeholder: '请输入订单日期'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '序列号ID',
        key: 'order_seq_id',
        sortable: true,
        treeNode: true,
        type: 'input',
        search: {
          disabled: false,
        },
        form: {
          editDisabled: true,
          rules: [
            // 表单校验规则
            { required: true, message: '订单序列号必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入订单序列号'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },

      {
        title: '订单ID',
        key: 'order_id',
        sortable: true,
        treeNode: true,
        type: 'input',
        search: {
          disabled: false,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '邀请码必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入订单ID'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },

      {
        title: '预计到达时间',
        key: 'arrival_time',
        show: false,
        type: 'datetime',
        // search: {
        //   disabled: false,
        // },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '订单日期必填' }
          ],
          component: {
            props: {
              'time-arrow-control': false,
              // 'picker-options': { shortcuts: shortcuts },
              format: 'yyyy-MM-dd HH:mm:ss',
              valueFormat: 'yyyy-MM-dd HH:mm:ss'
            },
            // placeholder: '请输入订单日期'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '订单地址',
        key: 'address',
        type: 'input',
        search: {
          disabled: true,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '邀请码必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            // placeholder: '请输入邀请码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '顾客名',
        key: 'recipient_name',
        type: 'input',
        search: {
          disabled: true,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '邀请码必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            // placeholder: '请输入邀请码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '隐私号码',
        key: 'privacy_phone',
        show: false,
        sortable: true,
        treeNode: true,
        type: 'input',
        search: {
          disabled: true,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '邀请码必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            // placeholder: '请输入邀请码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '备用隐私号码',
        key: 'backup_privacy_phones',
        show: false,
        sortable: true,
        treeNode: true,
        type: 'input',
        search: {
          disabled: true,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '邀请码必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            // placeholder: '请输入邀请码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '顾客电话',
        key: 'recipient_phone',
        show: false,
        sortable: true,
        treeNode: true,
        type: 'input',
        search: {
          disabled: true,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '邀请码必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            // placeholder: '请输入邀请码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '菜单信息',
        key: 'menu_json',
        sortable: true,
        treeNode: true,
        type: "textarea",
        show: false,
        search: {
          disabled: true,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '邀请码必填' }
          ],
          component: {
            span: 24,
            props: {
              type: "textarea",
              // autosize: true,
            },
            // placeholder: '请输入邀请码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '结算信息',
        key: 'settle_json',
        sortable: true,
        treeNode: true,
        type: "textarea",
        show: false,
        search: {
          disabled: true,
        },
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            // { required: true, message: '邀请码必填' }
          ],
          component: {
            span: 24,
            props: {
              type: "textarea",
              // autosize: true,
            },
            // placeholder: '请输入邀请码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
    ]
  }
}

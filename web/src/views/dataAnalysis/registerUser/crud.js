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
        title: '注册ID',
        key: 'id',
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
            { required: true, message: '注册ID必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入别名'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '微信openid',
        key: 'openid',
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
            { required: true, message: '微信openid必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入微信openid'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '姓名',
        key: 'username',
        sortable: true,
        treeNode: true,
        type: 'input',
        form: {
          editDisabled: false,
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入姓名'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '昵称',
        key: 'alias_name',
        sortable: true,
        treeNode: true,
        type: 'input',
        form: {
          editDisabled: false,
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入昵称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '手机号',
        key: 'telephone',
        sortable: true,
        treeNode: true,

        type: 'input',
        form: {
          editDisabled: false,
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入手机号'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
    ]
  }
}

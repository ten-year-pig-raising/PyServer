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
        title: '商铺名称',
        key: 'shop_name',
        sortable: true,
        treeNode: true,
        type: 'input',
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: '商铺名称必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入商铺名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '邀请码类型',
        key: 'shop_type',
        type: 'select',
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
        title: '商铺ID',
        key: 'shop_id',
        sortable: true,
        treeNode: true,
        type: 'input',
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: '商铺ID必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入商铺ID'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '商家地址',
        key: 'shop_addr',
        sortable: true,
        treeNode: true,
        type: 'input',
        form: {
          editDisabled: false,
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入商家地址'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '商家平均消费',
        key: 'shop_avg_price',
        sortable: true,
        treeNode: true,
        type: 'input',
        form: {
          editDisabled: false,
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入商家平均消费'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '邀请码',
        key: 'invitation_code',
        sortable: true,
        treeNode: true,
        type: 'input',
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
        title: '邀请人',
        key: 'inviter',
        sortable: true,
        treeNode: true,
        type: 'input',
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: '邀请人必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入邀请人'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'inviter_name'
        }
      },
      {
        title: '所属用户',
        key: 'register_user',
        sortable: true,
        treeNode: true,
        type: 'input',
        form: {
          editDisabled: false,
          rules: [
            // 表单校验规则
            { required: true, message: '所属用户必填' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入所属用户'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'register_username'
        }
      }
    ]
  }
}

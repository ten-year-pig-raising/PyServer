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
      defaultSpan: 24, // 默认的表单 span
      width: '35%'
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
        title: '邀请码',
        key: 'code',
        sortable: true,
        treeNode: true,

        type: 'input',
        form: {
          editDisabled: true,
          rules: [
            // 表单校验规则
            { required: true, message: '商品名称必填' }
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
        title: '邀请码类型',
        key: 'code_type',
        sortable: true,
        treeNode: true,

        type: 'input',
        form: {
          editDisabled: true,
          rules: [
            // 表单校验规则
            { required: true, message: '商品名称必填' }
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
        title: '生效开始时间',
        key: 'valid_start_time',
        sortable: true,
        treeNode: true,

        type: 'input',
        form: {
          editDisabled: true,
          rules: [
            // 表单校验规则
            { required: true, message: '商品名称必填' }
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
        title: '生效结束时间',
        key: 'valid_end_time',
        sortable: true,
        treeNode: true,

        type: 'input',
        form: {
          editDisabled: true,
          rules: [
            // 表单校验规则
            { required: true, message: '商品名称必填' }
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
      }
    ].concat(vm.commonEndColumns())
  }
}

<template>
  <div>
    <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
      <d2-crud-x
        ref="d2Crud"
        v-bind="_crudProps"
        v-on="_crudListeners"
        @customBtn2="showService"
      >
        <!-- 自动绑定参数与事件 -->
        <!-- 包含详细参数见：https://gitee.com/greper/d2-crud-plus/blob/master/packages/d2-crud-plus/src/lib/mixins/crud.js#L164-->
        <div slot="header">
          <crud-search
            ref="search"
            :options="crud.searchOptions"
            @submit="handleSearch"
          />
          <el-button-group>
            <el-button size="small" type="primary" @click="addRow"
              ><i class="el-icon-plus" /> 新增</el-button
            >
          </el-button-group>
          <crud-toolbar
            v-bind="_crudToolbarProps"
            v-on="_crudToolbarListeners"
          />
        </div>
      </d2-crud-x>
    </d2-container>
    <el-drawer
      title="店铺服务"
      :visible.sync="drawer"
      :direction="direction"
      size="50%"
    >
    <el-card class="box-card">
      <div>店铺名称:<span>{{shopInfo.shop_name}}</span></div>
      <div>店铺:<span>{{shopInfo.shop_id}}</span></div>
    </el-card>
      <el-table :data="shopInfo.shop_service" style="width: 100%; margin: 20px">
        <el-table-column prop="service_name" label="服务"> </el-table-column>
        <el-table-column prop="is_open" label="开关">
          <template slot-scope="scope">
            <el-switch
              v-model="scope.row.is_open"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-text="开"
              inactive-text="关"
            >
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column prop="record" label="记录"> </el-table-column>
        <el-table-column fixed="right" label="操作">
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row)" type="text" size="small"
              >查看</el-button
            >
            <el-button type="text" size="small">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- <div class="demo-drawer__footer">
        <el-button @click="cancelForm">取 消</el-button>
        <el-button
          type="primary"
          @click="$refs.drawer.closeDrawer()"
          :loading="loading"
          >{{ loading ? "提交中 ..." : "确 定" }}</el-button
        >
      </div> -->
    </el-drawer>
  </div>
</template>

<script>
import { crudOptions } from './crud' // 上文的crudOptions配置
import { d2CrudPlus } from 'd2-crud-plus'
import { AddObj, GetList, UpdateObj, DelObj, GetShop } from './api' // 查询添加修改删除的http请求接口
export default {
  name: 'Shop',
  mixins: [d2CrudPlus.crud], // 最核心部分，继承d2CrudPlus.crud
  data () {
    return {
      drawer: false,
      direction: 'rtl',
      shopInfo: {
        id: '',
        shop_id: '',
        shop_name: '',
        shop_type: '',
        shop_addr: '',
        shop_avg_price: '',
        shop_service: []
      },
      tableData: [
        {
          service_name: '评分计算',
          is_open: false,
          record: '4.9'
        },
        {
          service_name: '辅助出餐',
          is_open: false,
          record: '4.9'
        },
        {
          service_name: '辅助自配',
          is_open: false,
          record: '4.9'
        }
      ]
    }
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      return GetList(query)
    }, // 数据请求
    addRequest (row) {
      return AddObj(row)
    }, // 添加请求
    updateRequest (row) {
      return UpdateObj(row)
    }, // 修改请求
    delRequest (row) {
      return DelObj(row.id)
    }, // 删除请求
    showService (data) {
      this.drawer = !this.drawer
      GetShop(data.row.id).then(res => {
        this.shopInfo = res.data.data
        console.log(this.shopInfo)
      })
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then((_) => {
          done()
        })
        .catch((_) => {})
    }
  }
}
</script>
<style lang="scss">
.box-card {
  margin: 20px;
  div{
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
    span{
      font-family:'Courier New', Courier, monospace;
      font-size: 16px;
    }
  }
}
</style>

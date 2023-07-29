<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners">
      <!-- 自动绑定参数与事件 -->
      <!-- 包含详细参数见：https://gitee.com/greper/d2-crud-plus/blob/master/packages/d2-crud-plus/src/lib/mixins/crud.js#L164-->
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow">
            <i class="el-icon-plus" /> 新增
          </el-button>
        </el-button-group>
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" />
      </div>
    </d2-crud-x>
    <el-drawer
      title="同步店铺评论"
      :visible.sync="drawer"
      direction="rtl"
      :before-close="handleClose"
      size="50%"
    >
      <el-form
        ref="commentsConditionForm"
        :model="commentsCondition"
        label-width="80px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item label="店铺ID">
              <el-input v-model="commentsCondition.shop_code"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="店铺类型">
              <el-radio-group v-model="commentsCondition.shop_type">
                <el-radio label="meituan">美团</el-radio>
                <el-radio label="elm">饿了么</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="8">
            <el-form-item label="开始页码">
              <el-input v-model="commentsCondition.pageStart"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="结束页码">
              <el-input v-model="commentsCondition.pageEnd"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="每页大小">
              <el-input v-model="commentsCondition.pageSize"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">同步</el-button>
          <el-button>取消</el-button>
        </el-form-item>
      </el-form>
    </el-drawer>
  </d2-container>
</template>

<script>
import { crudOptions } from "./crud"; // 上文的crudOptions配置
import { d2CrudPlus } from "d2-crud-plus";
import { AddObj, GetList, UpdateObj, DelObj, getShopComments } from "./api"; // 查询添加修改删除的http请求接口
export default {
  name: "businessSession",
  mixins: [d2CrudPlus.crud], // 最核心部分，继承d2CrudPlus.crud
  data() {
    return {
      drawer: false,
      commentsCondition: {},
    };
  },
  methods: {
    getCrudOptions() {
      return crudOptions(this);
    },
    pageRequest(query) {
      return GetList(query);
    }, // 数据请求
    addRequest(row) {
      return AddObj(row);
    }, // 添加请求
    updateRequest(row) {
      return UpdateObj(row);
    }, // 修改请求
    delRequest(row) {
      return DelObj(row.id);
    }, // 删除请求
    openDrawer() {
      this.drawer = true;
    },
    handleClose(done) {
      done();
      //   this.$confirm('确认关闭？')
      //     .then(_ => {
      //       done()
      //     })
      //     .catch(_ => {})
    },
    onSubmit() {
      console.log(this.commentsCondition);
      getShopComments(this.commentsCondition).then((res) => {
        this.$message.success("成功");
      });
      console.log("submit!");
    },
  },
};
</script>

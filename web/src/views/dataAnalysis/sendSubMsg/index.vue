<template>
  <d2-container>
    <el-form :model="msg" :rules="rules" ref="ruleForm" label-width="100px">
      <el-form-item label="发送对象" prop="tousers">
        <el-tag
          v-for="selection in multipleSelection"
          :key="selection.key"
          closable
          type="success"
        >
          {{ selection.name }}
        </el-tag>
        <el-input v-show="msg.user_type == 'input'"  v-model="msg.tousers"></el-input>
      </el-form-item>
      <el-form-item label="对象类型">
        <el-radio-group v-model="msg.user_type" @change="userTypeChange">
          <el-radio label="shop">店铺</el-radio>
          <el-radio label="user">用户</el-radio>
          <el-radio label="input">手动输入</el-radio>
        </el-radio-group>
        <el-button
          v-show="msg.user_type != 'input'"
          class="showDialog-button"
          @click="showDialog"
          >选择发送对象</el-button
        >
      </el-form-item>
      <el-form-item label="参数1" prop="param1">
        <el-input v-model="msg.param1"></el-input>
      </el-form-item>
      <el-form-item label="参数2" prop="param2">
        <el-input v-model="msg.param2"></el-input>
      </el-form-item>
      <el-form-item label="参数3" prop="param3">
        <el-input v-model="msg.param3"></el-input>
      </el-form-item>
      <el-form-item label="参数4" prop="param4">
        <el-input v-model="msg.param4"></el-input>
      </el-form-item>
      <el-form-item label="参数5" prop="param5">
        <el-input v-model="msg.param5"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')"
          >发送</el-button
        >
        <!-- <el-button @click="resetForm('ruleForm')">重置</el-button> -->
      </el-form-item>
    </el-form>
    <el-dialog title="注册用户" :visible.sync="userDialogVisible" width="50%">
      <el-table
        ref="multipleUserTable"
        :data="userTableData.data"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleUserSelectionChange"
      >
        <el-table-column type="selection" width="55"> </el-table-column>
        <el-table-column prop="alias_name" label="别名"> </el-table-column>
        <el-table-column prop="openid" label="openid" show-overflow-tooltip>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleUserSizeChange"
        @current-change="handleUserCurrentChange"
        :current-page="userTableData.page"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="10"
        layout="total, sizes, prev, pager, next, jumper"
        :total="userTableData.total"
      >
      </el-pagination>
      <!-- <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false"
          >确 定</el-button
        >
      </span> -->
    </el-dialog>
    <el-dialog title="店铺" :visible.sync="shopDialogVisible" width="50%">
      <el-form :inline="true" :model="shopSearchForm" class="demo-form-inline">
        <el-form-item label="店铺名称">
          <el-input
            v-model="shopSearchForm.shop_name"
            placeholder="店铺名称"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="shopSearch">查询</el-button>
        </el-form-item>
      </el-form>
      <el-table
        ref="multipleShopTable"
        :data="shopTableData.data"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleShopSelectionChange"
      >
        <el-table-column type="selection" width="55"> </el-table-column>
        <el-table-column prop="shop_name" label="店铺名称"> </el-table-column>
        <el-table-column prop="shop_type_label" label="类型"> </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleShopSizeChange"
        @current-change="handleShopCurrentChange"
        :current-page="shopTableData.page"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="10"
        layout="total, sizes, prev, pager, next, jumper"
        :total="shopTableData.total"
      >
      </el-pagination>
    </el-dialog>
  </d2-container>
</template>

<script>
import { sendSubMsg } from "./api";
import { GetList } from "../registerUser/api"; // 查询添加修改删除的http请求接口
import { GetList as shopGetList } from "../shop/api";
import { v } from "vxe-table";
export default {
  name: "SendSubMsg",
  mounted() {},
  data() {
    return {
      userDialogVisible: false,
      multipleSelection: [],
      userTableData: {
        page: 1,
        total: 0,
        limit: 10,
        data: [],
      },
      shopDialogVisible: false,
      shopSearchForm: {
        shop_name: "",
      },
      shopTableData: {
        page: 1,
        total: 0,
        limit: 10,
        data: [],
      },
      msg: {
        tousers: "",
        user_type: "shop",
      },
      rules: {
        name: [
          { required: true, message: "请输入活动名称", trigger: "blur" },
          { min: 3, max: 5, message: "长度在 3 到 5 个字符", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          sendSubMsg(this.msg).then((res) => {
            // console.log(res)
            this.$message.success("发送成功");
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    showDialog() {
      if (this.msg.user_type == "user") {
        let params = {
          page: this.userTableData.page,
          limit: this.userTableData.limit,
        };
        this.getUserData(params);
        this.userDialogVisible = true;
        // console.log(this.multipleSelection);
      } else if (this.msg.user_type == "shop") {
        let params = {
          page: this.userTableData.page,
          limit: this.userTableData.limit,
        };
        this.getShopData(params);
        this.shopDialogVisible = true;
      }
    },
    userTypeChange(val) {
      // console.log(val)
      // 清除已选数据
      this.msg.tousers = "";
      this.multipleSelection = [];
    },
    getUserData(params) {
      GetList(params).then((rs) => {
        this.userTableData.data = rs.data.data;
        this.userTableData.page = rs.data.page;
        this.userTableData.limit = rs.data.limit;
        this.userTableData.total = rs.data.total;
      });
    },
    handleUserSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.userTableData.limit = val;
      let params = {
        page: this.userTableData.page,
        limit: val,
      };
      this.getUserData(params);
    },
    handleUserCurrentChange(val) {
      this.userTableData.page = val;
      let params = {
        page: val,
        limit: this.userTableData.limit,
      };
      this.getUserData(params);
    },
    handleUserSelectionChange(val) {
      if (val.length === 0) {
        return;
      }
      this.multipleSelection = [];
      let selectionStr;
      val.forEach((selection) => {
        if (selectionStr === undefined) {
          selectionStr = selection.openid;
        } else {
          selectionStr = selectionStr + ";" + selection.openid;
        }
        this.multipleSelection.push({
          key: selection.id,
          name: selection.openid,
          value: selection.openid,
        });
      });
      this.msg.tousers = selectionStr;
      // console.log(this.msg.touser);
    },
    getShopData(params) {
      shopGetList(params).then((rs) => {
        this.shopTableData.data = rs.data.data;
        this.shopTableData.page = rs.data.page;
        this.shopTableData.limit = rs.data.limit;
        this.shopTableData.total = rs.data.total;
        // shopTableData: {
        // page: 1,
        // total: 0,
        // limit: 10,
      });
    },
    shopSearch() {
      console.log("shopSearch");
      let params = {
        page: this.shopTableData.page,
        limit: this.shopTableData.limit,
        shop_name: this.shopSearchForm.shop_name,
      };
      this.getShopData(params);
    },
    handleShopSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.shopTableData.limit = val;
      let params = {
        page: this.shopTableData.page,
        limit: val,
      };
      this.getShopData(params);
    },
    handleShopCurrentChange(val) {
      this.shopTableData.page = val;
      let params = {
        page: val,
        limit: this.shopTableData.limit,
      };
      this.getShopData(params);
    },
    handleShopSelectionChange(val) {
      if (val.length === 0) {
        return;
      }
      let selectionStr;
      this.multipleSelection = [];
      val.forEach((selection) => {
        if (selectionStr === undefined) {
          selectionStr = selection.id;
        } else {
          selectionStr = selectionStr + ";" + selection.id;
        }
        this.multipleSelection.push({
          key: selection.id,
          name: selection.shop_name,
          value: selection.id,
        });
      });
      this.msg.tousers = selectionStr;
      // console.log(this.msg.tousers);
    },
  },
};
</script>
<style lang="scss">
.showDialog-button {
  margin-left: 20px;
}
</style>
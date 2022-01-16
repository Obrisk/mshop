<template>
    <div class="content-page">
        <div class="content-nav">
            <el-breadcrumb class="breadcrumb" separator="/">
                <el-breadcrumb-item :to="{ name: 'nature' }">Settings</el-breadcrumb-item>
                <el-breadcrumb-item>{{infoForm.id ? 'Edit Type' : 'New Type'}}</el-breadcrumb-item>
            </el-breadcrumb>
            <div class="operation-nav">
                <el-button type="primary" @click="goBackPage" icon="arrow-left">Back</el-button>
            </div>
        </div>
        <div class="content-main">
            <div class="form-table-box">
                <el-form ref="infoForm" :rules="infoRules" :model="infoForm" label-width="120px">
                    <el-form-item label="Category Name" prop="name">
                        <el-input v-model="infoForm.name"></el-input>
                    </el-form-item>
                    <el-form-item label="Sort">
                        <el-input-number v-model="infoForm.sort_order" :min="1" :max="1000"></el-input-number>
                    </el-form-item>
                    <el-form-item>
                        <el-button v-if="infoForm.id > 0" type="primary" @click="updateSpec">Submit</el-button>
                        <el-button v-else type="primary" @click="addSpec">Create Type</el-button>
                        <el-button v-if="infoForm.id > 0" type="danger" @click="specDelete">Delete</el-button>
                        <el-button @click="goBackPage">Cancel</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
    import api from '@/config/api';
    export default {
        data() {
            return {
                infoForm: {
                    id: 0,
                    name: "",
                    sort_order: 1,
                },
                infoRules:{
                    name: [
                        {required: true, message: 'Please enter the Name', trigger: 'blur'},
                    ]
                }
            }
        },
        methods: {
            addSpec(){
                let info = {
                    name:this.infoForm.name,
                    sort_order:this.infoForm.sort_order
                }
                this.$refs['infoForm'].validate((valid) => {
                    if (valid) {
                        this.axios.post('specification/add', info).then((response) => {
                            if (response.data.errno === 0) {
                                this.$message({
                                    type: 'success',
                                    message: 'Added New Type'
                                });
                                this.$router.go(-1);
                            } else {
                                this.$message({
                                    type: 'error',
                                    message: 'Failed to create Type, try later'
                                })
                            }
                        })
                    } else {
                        return false;
                    }
                });
            },
            updateSpec(){
                let info = {
                    id:this.infoForm.id,
                    name:this.infoForm.name,
                    sort_order:this.infoForm.sort_order
                }
                this.$refs['infoForm'].validate((valid) => {
                    if (valid) {
                        this.axios.post('specification/update', info).then((response) => {
                            if (response.data.errno === 0) {
                                this.$message({
                                    type: 'success',
                                    message: 'Updated Successfully'
                                });
                                this.$router.go(-1);
                            } else {
                                this.$message({
                                    type: 'error',
                                    message: 'Failed to update, try later'
                                })
                            }
                        })
                    } else {
                        return false;
                    }
                });
            },
            specDelete(index, row) {
                this.$confirm('Are you sure you want to Delete?', '提示', {
                    confirmButtonText: 'Confirm',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }).then(() => {
                    this.axios.post('specification/delete', {id: row.id}).then((response) => {
                        console.log(response.data)
                        if (response.data.errno === 0) {
                            this.$message({
                                type: 'success',
                                message: 'Deleted Successfully'
                            });
                            this.$router.go(-1);
                        }
                        else {
                            this.$message({
                                type: 'error',
                                message: 'Failed to Delete, try later!'
                            });
                        }
                    })
                });
            },
            goBackPage() {
                this.$router.go(-1);
            },
            getInfo() {
                console.log(this.infoForm.id);
            console.log(this.infoForm.id);
            console.log(this.infoForm.id);
                if (this.infoForm.id <= 0) {
                    return false
                }
                let that = this
                this.axios.post('specification/detail', {
                        id: that.infoForm.id
                }).then((response) => {
                    let resInfo = response.data.data;
                    console.log(resInfo);
                    that.infoForm = resInfo;
                })
            }
        },
        components: {},
        mounted() {
            this.infoForm.id = this.$route.query.id || 0;
            
            this.getInfo();
        }
    }

</script>

<style scoped>
    .image-uploader {
        height: 105px;
    }

    .image-uploader .el-upload {
        border: 1px solid #d9d9d9;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .image-uploader .el-upload:hover {
        border-color: #20a0ff;
    }

    .image-uploader .image-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        min-width: 105px;
        height: 105px;
        line-height: 105px;
        text-align: center;
    }

    .image-show {
        background-color: #f8f8f8;
        min-width: 105px;
        height: 105px;
        display: block;
    }

</style>

<template>
    <div class="content-page">
        <div class="content-nav">
            <el-breadcrumb class="breadcrumb" separator="/">
                <el-breadcrumb-item :to="{ name: 'nature' }">Settings</el-breadcrumb-item>
                <el-breadcrumb-item>{{infoForm.id ? 'Edit Category' : 'New Category'}}</el-breadcrumb-item>
            </el-breadcrumb>
            <div class="operation-nav">
                <el-button type="primary" @click="goBackPage" icon="arrow-left">Back</el-button>
            </div>
        </div>
        <div class="content-main">
            <div class="form-table-box">
                <el-form ref="infoForm" :rules="infoRules" :model="infoForm" label-width="120px">
                    <!-- <el-form-item label="上级分类" prop="name">
                        <el-select v-model="infoForm.parent_id" placeholder="请选择上级分类">
                            <el-option v-for="item in parentCategory" :key="item.id" :label="item.name"
                                       :value="item.id"></el-option>
                        </el-select>
                    </el-form-item> -->
                    <el-form-item label="Category Name" prop="name">
                        <el-input v-model="infoForm.name"></el-input>
                    </el-form-item>
                    <el-form-item label="Short Details">
                        <el-input type="textarea" v-model="infoForm.front_name" :rows="1"></el-input>
                        <div class="form-tip"></div>
                    </el-form-item>
                    <el-form-item label="Product Photo" prop="img_url" v-if="infoForm.parent_id == 0">
                        <img v-if="infoForm.img_url" :src="infoForm.img_url" class="image-show">
                        <el-upload
                                class="upload-demo"
                                name="file"
                                :action="qiniuZone"
                                :on-remove="bannerRemove"
                                :before-remove="beforeBannerRemove"
                                :file-list="fileList"
                                :on-success="handleUploadBannerSuccess"
                                :data="picData"
                                :before-upload="getQiniuToken"
                        >
                            <el-button v-if="!infoForm.img_url" size="small" type="primary">Choose Image</el-button>
                        </el-upload>
                        <div class="form-tip">Image size Max size is 690, Supports png/jpg</div>
                    </el-form-item>
                    <el-form-item label="Photo Height" prop="name" v-if="infoForm.parent_id == 0">
                        <el-input v-model="infoForm.p_height"></el-input>
                    </el-form-item>
                    <el-form-item label="Icon" prop="icon_url" v-if="infoForm.parent_id == 0">
                        <img v-if="infoForm.icon_url" :src="infoForm.icon_url" class="image-show">
                        <el-upload
                                class="upload-demo"
                                name="file"
                                :action="qiniuZone"
                                :on-remove="iconRemove"
                                :before-remove="beforeIconRemove"
                                :file-list="fileList2"
                                :data="picData"
                                :on-success="handleUploadIconSuccess"
                                :before-upload="getQiniuToken"
                        >
                            <el-button v-if="!infoForm.icon_url" size="small" type="primary">Choose Image</el-button>
                        </el-upload>

                        <div class="form-tip">Icon size 250*250, supports jpg/png</div>
                    </el-form-item>
                    <el-form-item label="Sort">
                        <el-input-number v-model="infoForm.sort_order" :min="1" :max="1000"></el-input-number>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmitInfo">Submit</el-button>
                        <el-button @click="goBackPage">Cancel</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
    import api from '@/config/api';
    import ElFormItem from "../../../../node_modules/element-ui/packages/form/src/form-item.vue";

    export default {
        data() {
            return {
                root: '',
                qiniuZone:'',
                fileList: [],
                fileList2: [],
                parentCategory: [
                    {
                        id: 0,
                        name: '顶级分类'
                    }
                ],
                infoForm: {
                    id: 0,
                    name: "",
                    parent_id: 0,
                    front_name: '',
                    img_url: '',
                    sort_order: 100,
                    icon_url:''
                    // is_show: true,
                },
                infoRules: {
                    name: [
                        {required: true, message: 'Name is required', trigger: 'blur'},
                    ],
                    front_name: [
                        {required: true, message: 'Introduction is required', trigger: 'blur'},
                    ],
                    img_url: [
                        {required: true, message: 'Photo is required', trigger: 'blur'},
                    ],
                    icon_url: [
                        {required: true, message: 'Icon is required', trigger: 'blur'},
                    ],
                },
                picData: {
                    token: ''
                },
                url: ''
            }
        },
        methods: {
            getQiniuToken() {
                let that = this
                this.axios.post('index/getQiniuToken').then((response) => {
                    let resInfo = response.data.data;
                    that.picData.token = resInfo.token;
                    that.url = resInfo.url;
                })
            },
            beforeBannerRemove(file, fileList) {
                return this.$confirm(`Are you sure you want to completely remove this image?`);
            },
            beforeIconRemove(file, fileList) {
                return this.$confirm(`Are you sure you want to completely remove this icon?`);
            },
            bannerRemove(file, fileList) {
                this.infoForm.img_url = '';
                let id = this.infoForm.id;
                this.axios.post('category/deleteBannerImage', {id: id}).then((response) => {
                    this.$message({
                        type: 'success',
                        message: 'Deleted Successfully'
                    });
                });
            },
            iconRemove(file, fileList) {
                this.infoForm.icon_url = '';
                let id = this.infoForm.id;
                this.axios.post('category/deleteIconImage', {id: id}).then((response) => {
                    this.$message({
                        type: 'success',
                        message: 'Deleted Successfully'
                    });
                });
            },
            goBackPage() {
                this.$router.go(-1);
            },
            onSubmitInfo() {
                this.infoForm.level = this.infoForm.parent_id == 0 ? 'L1' : 'L2';
                this.$refs['infoForm'].validate((valid) => {
                    if (valid) {
                        this.axios.post('category/store', this.infoForm).then((response) => {
                            if (response.data.errno === 0) {
                                this.$message({
                                    type: 'success',
                                    message: 'Uploaded successfully'
                                });
                                this.$router.go(-1)
                            } else {
                                this.$message({
                                    type: 'error',
                                    message: 'Failed to create'
                                })
                            }
                        })
                    } else {
                        return false;
                    }
                });
            },
            handleUploadBannerSuccess(res, file) {
                let url = this.url;
                this.infoForm.img_url = url + res.key;
            },
            handleUploadIconSuccess(res, file) {
                let url = this.url;
                this.infoForm.icon_url = url + res.key;
            },
            getTopCategory() {
                this.axios.get('category/topCategory').then((response) => {
                    this.parentCategory = this.parentCategory.concat(response.data.data);
                })
            },
            getInfo() {
                if (this.infoForm.id <= 0) {
                    return false
                }
                //加载分类详情
                let that = this
                this.axios.get('category/info', {
                    params: {
                        id: that.infoForm.id
                    }
                }).then((response) => {
                    let resInfo = response.data.data;
                    console.log(resInfo);
                    let data = {
                        name: '分类图',
                        url: resInfo.img_url
                    };
                    this.fileList.push(data);
                    let iconData = {
                        name: 'Icon',
                        url: resInfo.icon_url
                    };
                    this.fileList2.push(iconData);
                    that.infoForm = resInfo;
                })
            }

        },
        components: {ElFormItem},
        mounted() {
            this.getTopCategory();
            this.infoForm.id = this.$route.query.id || 0;
            this.getInfo();
            this.root = api.rootUrl;
            this.qiniuZone = api.qiniu;
            this.getQiniuToken();
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

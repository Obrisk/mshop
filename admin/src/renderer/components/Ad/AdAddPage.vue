<template>
    <div class="content-page">
        <div class="content-nav">
            <el-breadcrumb class="breadcrumb" separator="/">
                <el-breadcrumb-item :to="{ name: 'ad' }">Ads List</el-breadcrumb-item>
                <el-breadcrumb-item>{{infoForm.id ? 'EditAds' : 'Add NewAds'}}</el-breadcrumb-item>
            </el-breadcrumb>
            <div class="operation-nav">
                <!--<el-button type="primary" @click="test" icon="arrow-left">test</el-button>-->
                <el-button type="primary" @click="goBackPage" icon="arrow-left">Back</el-button>
            </div>
        </div>
        <div class="content-main">
            <div class="form-table-box">
                <el-form ref="infoForm" :rules="infoRules" :model="infoForm" label-width="120px">
					<el-form-item label="Ads Photo" prop="image_url" v-if="infoForm.image_url" class="image-uploader-diy new-height">
						<div class="index-image">
							<el-image :preview-src-list="previewList" v-if="infoForm.image_url" :src="infoForm.image_url" @click="previewIndexImg"
							 class="image-show" fit="cover"></el-image>
							<div class="o-shadow" @click="delePicList">
								<i class="el-icon-delete"></i>
							</div>
						</div>
					</el-form-item>
					<el-form-item label="Ads Photo" prop="image_url" v-if="!infoForm.image_url">
						<el-upload name="file" ref="upload" class="upload-demo" :action="qiniuZone" :on-success="handleSuccess"
						 :before-upload="getQiniuToken" :auto-upload="true" list-type="picture-card" :data="picData" :http-request="uploadIndexImg">
							<el-button size="small" type="primary">Upload</el-button>
							<div slot="tip" class="el-upload__tip">Only jpg/png Files</div>
						</el-upload>
					</el-form-item>
                    <el-form-item label="Product Type">
                        <el-radio-group v-model="infoForm.link_type">
                            <el-radio :label="0">Product id</el-radio>
                            <el-radio :label="1">Link</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="Ads Link" prop="link" v-if="infoForm.link_type == 1">
                        <el-input class="link-input" v-model="infoForm.link"></el-input>
                    </el-form-item>
                    <el-form-item label="Productid" prop="link" v-if="infoForm.link_type == 0">
                        <el-input class="id-input" v-model="infoForm.goods_id"></el-input>
                        <el-popover
                                placement="right"
                                v-model="related_pop"
                        >
                            <el-table :data="chooseRelateGoods" stripe style="width: 100%">
                                <el-table-column prop="id" label="id" width="100"></el-table-column>
                                <el-table-column prop="list_pic_url" label="Product Gallery" width="150">
                                    <template scope="scope">
                                        <img :src="scope.row.list_pic_url" alt="" style="width: 40px;height: 40px">
                                    </template>
                                </el-table-column>
                                <el-table-column prop="name" label="Product Name" width="300px"></el-table-column>
                                <el-table-column label="Action">
                                    <template scope="scope">
                                        <el-button
                                                size="small"
                                                type="danger"
                                                @click="relateSelect(scope.row.id)">Choose
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                            <el-button slot="reference" type="primary" @click="relateGoodsClick">Add Linked Product</el-button>
                        </el-popover>
                    </el-form-item>
                    <el-form-item label="End Date" prop="end_time">
                        <el-date-picker
                                v-model="infoForm.end_time"
                                type="datetime"
                                placeholder="Expiry Date"
                                default-time="23:59:59">
                            >
                        </el-date-picker>
                    </el-form-item>
                    <el-form-item label="Sort" prop="sort_order">
                        <el-input-number v-model="infoForm.sort_order" :min="1" :max="999"></el-input-number>
                    </el-form-item>
                    <el-form-item label="Turn On">
                        <el-switch active-value="1" inactive-value="0" v-model="infoForm.enabled"></el-switch>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmitInfo">Save</el-button>
                        <el-button @click="goBackPage">Cancel</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
    import api from '@/config/api';
	import lrz from 'lrz'
	import moment from 'moment'
    export default {
        data() {
            return {
                qiniuZone:'',
                root: '',
                fileList: [],
                infoForm: {
                    id: 0,
                    image_url: '',
                    link_type: 0,
                    enabled: 0,
                    end_time: '',
                    goods_id:0,
                    link:''
                },
                infoRules: {
                    image_url: [
                        {required: true, message: 'Please Add the Picture', trigger: 'blur'},
                    ],
                    end_time: [
                        {required: true, message: 'Please select Expiry Time', trigger: 'blur'},
                    ],
                },
                picData: {
                    token: ''
                },
                url: '',
                chooseRelateGoods: [],
                related_pop: false,
				previewList: [],
            }
        },
        methods: {
			handleSuccess(){},
			previewIndexImg() {
				let that = this;
				that.previewList = [];
				that.previewList.push(that.infoForm.image_url);
			},
			delePicList() {
				let that = this;
				that.$confirm('Are you sure you want to Delete?', 'Prompt', {
						confirmButtonText: 'Confirm',
						cancelButtonText: 'Cancel',
						type: 'warning'
					})
					.then(() => {
						that.infoForm.image_url = '';
					})
					.catch(() => {})
			},
			uploadIndexImg(request) {
				const file = request.file;
				lrz(file).then((rst) => {
					const config = {
						headers: {
							'Content-Type': 'multipart/form-data'
						},
					};
					const fileName = moment().format('YYYYMMDDHHmmssSSS') + Math.floor(Math.random() * 100) + file.name; //自定义图片名
					const formData = new FormData();
					formData.append('file', rst.file);
					formData.append('token', this.picData.token);
					formData.append('key', fileName);
					this.$http.post(this.qiniuZone, formData, config).then((res) => {
						this.handleUploadImageSuccess(res.data)
					})
				}).catch(function(err){
					console.log(err)
				})
			},
			handleUploadImageSuccess(res, file) {
			    let url = this.url;
			    this.infoForm.image_url = url + res.key;
			},
            relateSelect(id) {
                console.log(id);
                this.infoForm.goods_id = id;
                this.related_pop = false;
            },
            relateGoodsClick() {
                this.axios.post('ad/getallrelate', {id: this.infoForm.id}).then((response) => {
                    if (response.data.errno === 0) {
                        this.chooseRelateGoods = response.data.data
                    }
                });
            },
            test() {
                console.log(this.infoForm.end_time);
            },
            beforeAdRemove() {
                return this.$confirm(`Are you sure you want to Delete?`);
            },
            adRemove(file, fileList) {
                this.infoForm.image_url = '';
            },
            getQiniuToken() {
                let that = this
                this.axios.post('index/getQiniuToken').then((response) => {
                    let resInfo = response.data.data;
                    console.log(resInfo);
                    that.picData.token = resInfo.token;
                    that.url = resInfo.url;
                })
            },
            goBackPage() {
                this.$router.go(-1);
            },
            onSubmitInfo() {
                console.log(this.infoForm);
                // return false;
                let time = this.infoForm.end_time
                if (time == 0) {
                    this.$message({
                        type: 'error',
                        message: 'Please choose the Expiry Time'
                    });
                    return false;
                }
                if (this.infoForm.link_type == 0) {
                    if(this.infoForm.goods_id == 0 ){
                        this.$message({
                            type: 'error',
                            message: 'Please Choose Product'
                        });
                        return false;
                    }
                }
                if (this.infoForm.link_type == 1) {
                    if(this.infoForm.link == '' ){
                        this.$message({
                            type: 'error',
                            message: 'Please choose the link'
                        });
                        return false;
                    }
                }
                this.$refs['infoForm'].validate((valid) => {
                    if (valid) {
                        this.axios.post('ad/store', this.infoForm).then((response) => {
                            if (response.data.errno === 0) {
                                this.$message({
                                    type: 'success',
                                    message: 'Uploaded Successfully'
                                });
                                this.$router.go(-1);
                            } else if (response.data.errno === 100) {
                                this.$message({
                                    type: 'error',
                                    message: 'This Product has an Ad already'
                                })
                            }
                            else {
                                this.$message({
                                    type: 'error',
                                    message: 'Failed to Save'
                                })
                            }
                        })
                    } else {
                        return false;
                    }
                });
            },
            getInfo() {
                if (this.infoForm.id <= 0) {
                    return false
                }
                //加载Ads详情
                let that = this
                this.axios.get('ad/info', {
                    params: {
                        id: that.infoForm.id
                    }
                }).then((response) => {
                    let resInfo = response.data.data;
                    resInfo.enabled = resInfo.enabled ? "1" : "0";
                    that.infoForm = resInfo;
                    that.infoForm.end_time = resInfo.end_time * 1000;
                    let info = {
                        name: resInfo.name,
                        url: resInfo.image_url
                    };
                    this.fileList.push(info);
                    console.log(this.infoForm);
                })
            }
        },
        components: {},
        mounted() {
            this.infoForm.id = this.$route.query.id || 0;
            this.getInfo();
            this.root = api.rootUrl;
            this.getQiniuToken();
            this.qiniuZone = api.qiniu;
        }
    }

</script>

<style scoped>
    .image-show {
		width: 375px;
		height: 220px;
		background-color: #f9f9f9;
		display: block;
	}

    .id-input {
        margin-bottom: 20px;
    }

    .link-input .el-input__inner {
        width: 400px !important;
    }
	
	.o-shadow {
		position: absolute;
		bottom: 10px;
		right: 10px;
		background-color: rgba(0, 0, 0, .5);
		opacity: 0;
		transition: opacity .3s;
		color: #fff;
		font-size: 20px;
		line-height: 20px;
		padding: 10px;
		cursor: pointer;
	}
	
	.index-image {
		width: 375px;
		height: 220px;
		position: relative;
	}
	
	.index-image:hover .o-shadow {
		opacity: 1;
	}
</style>

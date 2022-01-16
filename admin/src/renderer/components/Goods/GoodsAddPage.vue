<template>
	<div class="content-page">
		<div class="content-nav">
			<el-breadcrumb class="breadcrumb" separator="/">
				<el-breadcrumb-item :to="{ name: 'goods' }">Products</el-breadcrumb-item>
				<el-breadcrumb-item>{{infoForm.id ? 'EditProduct' : 'New Product'}}</el-breadcrumb-item>
			</el-breadcrumb>
			<div class="operation-nav">
				<!-- <el-button type="primary" @click="test">测试</el-button> -->
				<el-button type="primary" @click="onSubmitInfo">Submit</el-button>
				<el-button @click="goBackPage" icon="arrow-left">Back</el-button>
			</div>
		</div>
		<div class="content-main">
			<div class="form-table-box">
				<el-form ref="infoForm" :rules="infoRules" :model="infoForm" label-width="120px">
					<el-form-item label="Categories">
						<el-select class="el-select-class" v-model="cateId" placeholder="Choose Category">
							<el-option v-for="item in cateOptions" :key="item.value" :label="item.label" :value="item.value">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="Default Photo" prop="list_pic_url" v-if="infoForm.list_pic_url" class="image-uploader-diy new-height">
						<div class="index-image">
							<el-image :preview-src-list="previewList" v-if="infoForm.list_pic_url" :src="infoForm.list_pic_url" @click="previewIndexImg"
							 class="image-show" fit="cover"></el-image>
							<div class="o-shadow" @click="delePicList">
								<i class="el-icon-delete"></i>
							</div>
						</div>
					</el-form-item>
					<el-form-item label="Photo" prop="list_pic_url" v-if="!infoForm.list_pic_url">
						<el-upload name="file" ref="upload" class="upload-demo" :action="qiniuZone" :on-success="handleSuccess"
						 :before-upload="indexImgBefore" :auto-upload="true" list-type="picture-card" :data="picData" :http-request="uploadIndexImg">
							<el-button size="small" type="primary">Upload</el-button>
							<div slot="tip" class="el-upload__tip">Only jpg/png is allowed</div>
						</el-upload>
					</el-form-item>
					<el-form-item label="Gallery Photos" prop="goods_sn">
						<draggable v-model="gallery_list" draggable=".gallery-item" class="drag-wrap">
							<div v-for="(element, index) in gallery_list" class="gallery-item" v-if="element.is_delete == 0">
								<el-image :preview-src-list="previewList" @click="previewImg(index)" style="width: 148px; height: 148px;margin:0 10px 10px 0;"
								 :src="element.url" fit="cover"></el-image>
								<div class="shadow" @click="onRemoveHandler(index)">
									<i class="el-icon-delete"></i>
								</div>
							</div>
							<el-upload name="file" ref="upload" :on-remove="galleryRemove" class="upload-demo" :action="qiniuZone"
							 :on-preview="galleryPreview" :show-file-list="false" :data="picData" :before-upload="galleryBefore" :on-error="hasErrorAct"
							 :on-success="handleSuccess" :auto-upload="true" multiple list-type="picture-card" :http-request="uploadGalleryImg">
								<i class="el-icon-plus"></i>
							</el-upload>
						</draggable>
					</el-form-item>
					<el-form-item label="Product Name" prop="name">
						<el-input v-model="infoForm.name"></el-input>
					</el-form-item>
					<el-form-item label="Short Title" prop="goods_brief">
						<el-input type="textarea" v-model="infoForm.goods_brief" :rows="3"></el-input>
						<div class="form-tip"></div>
					</el-form-item>
					<el-form-item label="Product Unit" prop="goods_unit">
						<el-input v-model="infoForm.goods_unit"></el-input>
						<div class="form-tip">Optional</div>
					</el-form-item>
					<el-form-item label="Sales Volume" prop="sell_volume">
						<el-input v-model="infoForm.sell_volume"></el-input>
					</el-form-item>
					<el-form-item label="Product Type">
						<div>
							<el-select class="el-select-class" v-model="specValue" placeholder="Product Type">
								<el-option v-for="item in specOptionsList" :key="item.value" :label="item.label" :value="item.value">
								</el-option>
							</el-select>
						</div>
						<div class="spec-wrap">
							<el-table :data="specData" stripe style="width: 100%">
								<el-table-column prop="goods_sn" label="Product SKU" width="140">
									<template scope="scope">
										<el-input @blur="checkSkuOnly(scope.$index, scope.row)" size="mini" v-model="scope.row.goods_sn" placeholder="ProductSKU"></el-input>
									</template>
								</el-table-column>
								<el-table-column prop="goods_aka" label="Short Title" width="160">
									<template scope="scope">
										<el-input size="mini" v-model="scope.row.goods_name" placeholder="Short title"></el-input>
									</template>
								</el-table-column>
								<el-table-column prop="value" label="Volume" width="130">
									<template scope="scope">
										<el-input size="mini" v-model="scope.row.value" placeholder="Bottle Volume"></el-input>
									</template>
								</el-table-column>
								<el-table-column prop="cost" label="Price" width="100">
									<template scope="scope">
										<el-input size="mini" v-model="scope.row.cost" placeholder="Price"></el-input>
									</template>
								</el-table-column>
								<el-table-column prop="retail_price" label="Retail Price" width="100">
									<template scope="scope">
										<el-input size="mini" v-model="scope.row.retail_price" placeholder="零售"></el-input>
									</template>
								</el-table-column>
								<el-table-column prop="goods_weight" label="Weight(KG)" width="100">
									<template scope="scope">
										<el-input size="mini" v-model="scope.row.goods_weight" placeholder="Weight"></el-input>
									</template>
								</el-table-column>
								<el-table-column prop="goods_number" label="Stock" width="100">
									<template scope="scope">
										<el-input size="mini" v-model="scope.row.goods_number" placeholder="Stock number"></el-input>
									</template>
								</el-table-column>
								<el-table-column label="Action" width="70">
									<template scope="scope">
										<el-button size="mini" type="danger" icon="el-icon-delete" circle @click="specDelete(scope.$index, scope.row)">
										</el-button>
									</template>
								</el-table-column>
							</el-table>
							<el-button class="marginTop20" type="primary" @click="addSpecData">Add Type</el-button>
						</div>
					</el-form-item>
					<el-form-item label="Imported" class="checkbox-wrap">
						<el-checkbox-group v-model="infoForm.is_new" class="checkbox-list">
							<el-checkbox label="Yes" name="is_new"></el-checkbox>
						</el-checkbox-group>
					</el-form-item>
					<el-form-item label="Express Delivery">
						<el-select v-model="kdValue" placeholder="Express Delivery Company" @change="kdChange">
							<el-option v-for="item in kdOptions" :key="item.value" :label="item.label" :value="item.value">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="Sort" prop="sort_order">
						<el-input-number :mini="1" :max="100" v-model="infoForm.sort_order"></el-input-number>
					</el-form-item>
					<el-form-item label="Stock">
						<el-switch active-text="Selling" inactive-text="Out of Stock" active-value="1" inactive-value="0" v-model="infoForm.is_on_sale"></el-switch>
					</el-form-item>
					<el-form-item label="Description" prop="goods_desc">
						<div class="edit_container">
							<quill-editor v-model="infoForm.goods_desc" ref="myTextEditor" class="editer" :options="editorOption" @blur="onEditorBlur($event)"
							 @ready="onEditorReady($event)">
							</quill-editor>
						</div>
					</el-form-item>
					<!-- 图片上传组件辅助-->
					<el-form-item class="upload_ad">
						<el-upload ref="upload" name="file" class="avatar-uploader" :action="qiniuZone" list-type="picture-card"
						 :file-list="detail_list" :before-upload="beforeUpload" :on-success="handleSuccess" :data="picData" multiple
						 :http-request="uploadDetailsImg">
						</el-upload>
					</el-form-item>
					<el-form-item>
						<el-button type="primary" @click="onSubmitInfo">Save</el-button>
						<el-button @click="goBackPage">Back</el-button>
						<el-button type="danger" class="float-right" @click="onCopyGood" v-if="infoForm.id > 0">Copy Product Info</el-button>
					</el-form-item>
				</el-form>
			</div>
		</div>
		<el-dialog :visible.sync="dialogVisible" size="tiny">
			<img width="100%" :src="dialogImageUrl" alt="">
		</el-dialog>
	</div>
</template>

<script>
	import api from '@/config/api';
	import lrz from 'lrz'
	import moment from 'moment'
	import draggable from 'vuedraggable'
	import $ from 'jquery'
	import {
		quillEditor
	} from 'vue-quill-editor'
	import ElForm from "../../../../node_modules/element-ui/packages/form/src/form.vue";
	import ElFormItem from "../../../../node_modules/element-ui/packages/form/src/form-item.vue"; //调用富文本Edit器
	const toolbarOptions = [
		['bold', 'italic', 'underline', 'strike'],
		['blockquote'],
		[{
			'list': 'ordered'
		}, {
			'list': 'bullet'
		}],
		[{
			'indent': '-1'
		}, {
			'indent': '+1'
		}],
		[{
			'size': ['small', false, 'large', 'huge']
		}],
		[{
			'header': [1, 2, 3, 4, 5, 6, false]
		}],
		['link', 'image', 'video']
	]
	export default {
		data() {
			return {
				root: '',
				qiniuZone: '',
				picData: {
					token: ''
				},
				url: '',
				kdOptions: [],
				kdValue: '',
				cateId: '',
				detail_list: [],
				dialogImageUrl: '',
				dialogVisible: false,
				options: [],
				cateOptions: [],
				editorOption: {
					modules: {
						toolbar: {
							container: toolbarOptions, // 工具栏
							handlers: {
								'image': function(value) {
									if (value) {
										document.querySelector('.avatar-uploader input').click()
									} else {
										this.quill.format('image', false);
									}
								}
							}
						},
						syntax: {
							highlight: text => hljs.highlightAuto(text).value
						}
					}
				},
				category: [],
				infoForm: {
					name: "",
					list_pic_url: '',
					goods_brief: '',
					goods_desc: '',
					is_on_sale: 0,
					is_new: false,
					// is_index: false,
				},
				infoRules: {
					name: [{
						required: true,
						message: 'Please Enter Name',
						trigger: 'blur'
					}, ],
					goods_brief: [{
						required: true,
						message: 'Please Enter Description',
						trigger: 'blur'
					}, ],
					list_pic_url: [{
						required: true,
						message: 'Please Add Product Picture',
						trigger: 'blur'
					}, ],
				},
				specRules: {
					value: [{
						required: true,
						message: 'Please Enter the Product Type',
						trigger: 'blur'
					}, ],
				},
				specData: [{
					goods_sn: '',
					value: '',
					cost: '',
					retail_price: '',
					goods_weight: '',
					goods_number: ''
				}],
				specOptionsList: [],
				specValue: 1,
				selectedSpec: '规格',
				is_has_spec: false,
				gallery: {
					goods_id: 0,
				},
				gallery_list: [],
				visible: false,
				hasPost: 0,
				previewList: [],
				autoFocus: false,
			}
		},
		methods: {
			handleSuccess() {},
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
						this.handleUploadListSuccess(res.data)
					})
				}).catch(function(err) {
					console.log(err)
				})
			},
			handleUploadListSuccess(res) {
				let url = this.url;
				this.infoForm.list_pic_url = url + res.key;
				console.log(this.infoForm.list_pic_url);
				this.axios.post('goods/uploadHttpsImage', {
					url: this.infoForm.list_pic_url
				}).then((response) => {
					let lastUrl = response.data.data;
					this.infoForm.https_pic_url = lastUrl;
				})
			},
			onRemoveHandler(index) {
				let that = this;
				that.$confirm('Delete This Picture?', 'Prompt', {
						confirmButtonText: 'Confirm',
						cancelButtonText: 'Cancel',
						type: 'warning'
					})
					.then(() => {
						let arr = that.gallery_list;
						arr[index].is_delete = 1;
					})
					.catch(() => {})
			},
			uploadGalleryImg(request) {
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
						this.handleUploadGallerySuccess(res.data)
					})
				}).catch(function(err) {
					console.log(err)
				})
			},
			handleUploadGallerySuccess(res) {
				let url = this.url;
				let urlData = url + res.key;
				let data = {
					id: 0,
					url: urlData,
					is_delete: 0,
				}
				this.gallery_list.push(data);
			},
			test() {
				console.log(this.gallery_list);
			},
			previewIndexImg() {
				let that = this;
				that.previewList = [];
				that.previewList.push(that.infoForm.list_pic_url);
			},
			previewImg(index) {
				let that = this;
				that.previewList = [];
				let arr = that.gallery_list;
				that.previewList.push(arr[index].url);
			},
			beforeRemove(file, fileList) {
				return this.$confirm(`Confirm to remove ${ file.name }？`);
			},
			checkSkuOnly(index, row) {
				console.log(index);
				console.log(row);
				if (row.goods_sn == '') {
					this.$message({
						type: 'error',
						message: 'Produc SKU is required'
					})
					return false;
				}
				this.axios.post('goods/checkSku', {
					info: row
				}).then((response) => {
					if (response.data.errno === 100) {
						this.$message({
							type: 'error',
							message: 'This SKU Already Exist'
						})
					} else {
						this.$message({
							type: 'success',
							message: 'SKU Updated Successfully'
						})
					}
				})
			},
			getSpecData() {
				let id = this.infoForm.id;
				this.axios.post('specification/getGoodsSpec', {
					id: id
				}).then((response) => {
					if (response.data.errno === 0) {
						let info = response.data.data;
						this.specData = info.specData;
						this.specValue = info.specValue;
					}
				})
			},
			addSpecData() {
				let ele = {
					goods_sn: '',
					value: '',
					cost: '',
					retail_price: '',
					goods_weight: '',
					goods_number: ''
				}
				this.specData.push(ele)
			},
			specDelete(index, row) {
				this.specData.splice(index, 1);
			},
			testCallBack() {
				console.log(this.specValue);
			},
			hasErrorAct(err) {
				console.log(err);
			},
			getQiniuToken() {
				let that = this
				this.axios.post('index/getQiniuToken').then((response) => {
					let resInfo = response.data.data;
					that.picData.token = resInfo.token;
					that.url = resInfo.url;
				})
			},
			specChange(value) {
				this.specForm.id = value;
			},
			addPrimarySpec() {
				this.is_has_spec = true;
			},
			getImgUrl() {
				let str = this.infoForm.goods_desc;
				//匹配图片（g表示匹配所有结果i表示区分大小写）
				let imgReg = /<img [^>]*src=['"]([^'"]+)[^>]*>/gi;
				//匹配src属性
				let srcReg = /src=[\'\"]?([^\'\"]*)[\'\"]?/i;
				let arr = str.match(imgReg);
				if (arr == null) {
					return false;
				}
				let data = [];

				for (let i = 0; i < arr.length; i++) {
					let src = arr[i].match(srcReg);
					let jsonData = {};
					jsonData.url = src[1];
					data[i] = jsonData;
				}
				this.detail_list = data;

			},
			submitUpload() {
				this.$refs.upload.submit();
			},
			delePicList() {
				let that = this;
				that.$confirm('Are you sure you want to Delete?', 'Prompt', {
						confirmButtonText: 'Confirm',
						cancelButtonText: 'Cancel',
						type: 'warning'
					})
					.then(() => {
						that.infoForm.list_pic_url = '';
					})
					.catch(() => {})
			},
			indexImgBefore(file) {
				this.getQiniuToken();
			},
			galleryBefore(file) {
				this.picData.key = new Date().getTime() + Math.floor(Math.random() * 100) + file.name; //自定义图片名
				this.getQiniuToken();
			},
			galleryRemove(file, fileList) {
				console.log(file);
				console.log(fileList);
			},
			galleryPreview(file) {
				console.log(file);
				this.dialogImageUrl = file.url;
				this.dialogVisible = true;
			},
			getGalleryList() {
				let goodsId = this.infoForm.id;
				this.axios.post('goods/getGalleryList', {
					goodsId: goodsId
				}).then((response) => {
					this.gallery_list = response.data.data.galleryData;
				})
			},
			kdChange(kdValue) {
				this.infoForm.freight_template_id = kdValue;
			},
			timeChange(val) {
				console.log(val);
				// this.infoForm.freight_template_id = kdValue;
			},
			onEditorReady(editor) {
				console.log('editor ready!', editor)
			},
			onEditorFocus(editor) {
				console.log('editor focus!', editor)
			},
			onEditorBlur(editor) {
				console.log('editor blur!', editor)
			},

			beforeUpload(file) {
				this.getQiniuToken();
				this.quillUpdateImg = true
			},
			uploadError() {
				// loading动画消失
				this.quillUpdateImg = false
				this.$message.error('Image Insertion Failed')
			},
			goBackPage() {
				this.$router.go(-1);
			},
			//富文本插入网络图片
			onLinkImageUrl() {
				var imageurl = document.querySelector('.url-image-fuzhu input').value
				let quill = this.$refs.myTextEditor.quill
				let length = quill.getSelection().index;
				quill.insertEmbed(length, 'image', imageurl)
				quill.setSelection(length + 1)
			},
			onCopyGood() {
				this.$confirm('Are you sure you want to copy this Product?', 'Prompt', {
					confirmButtonText: 'Confirm',
					cancelButtonText: 'Cancel',
					type: 'warning'
				}).then(() => {
					this.axios.post('goods/copygoods', {
						id: this.infoForm.id
					}).then((response) => {
						if (response.data.errno === 0) {
							this.$message({
								type: 'success',
								message: 'Copy Successfully'
							});
							//                            this.is_has_spec = false;
							//                            this.specData = [];
						}
					})
				});
			},
			onSubmitInfo() {
				this.$refs['infoForm'].validate((valid) => {
					if (valid) {
						if (this.infoForm.list_pic_url == '' || this.infoForm.list_pic_url == null) {
							this.$message({
								type: 'error',
								message: 'Please Upload the Default Image of the product'
							})
							return false;
						}
						if (this.gallery_list.length == 0) {
							this.$message({
								type: 'error',
								message: 'Please Upload at least 1 gallery photo'
							})
							return false;
						}
						if (this.specData.length == 0) {
							this.$message({
								type: 'error',
								message: 'Please Add New Type'
							})
							return false;
						}
						for (const ele of this.specData) {
							if (ele.cost == '' || ele.goods_sn == '' || ele.goods_weight == '' || ele.retail_price == '' || ele.value ==
								'') {
								this.$message({
									type: 'error',
									message: 'Type or Price value cannot be empty'
								})
								return false;
							}
						}
						this.infoForm.gallery = this.gallery_list;
						// return false;
						this.axios.post('goods/store', {
							info: this.infoForm,
							specData: this.specData,
							specValue: this.specValue,
							cateId: this.cateId,
						}).then((response) => {
							if (response.data.errno === 0) {
								this.$message({
									type: 'success',
									message: 'Saved Successfully'
								});
								this.infoForm.id = response.data.data;
								this.getGalleryList();
								// this.$router.go(-1);
							} else {
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
			uploadDetailsImg(request) {
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
						this.handleUploadDetailSuccess(res.data)
					})
				}).catch(function(err) {
					console.log(err)
				})
			},
			handleUploadDetailSuccess(res) {
				let url = this.url;
				let data = url + res.key;
				let quill = this.$refs.myTextEditor.quill
				// 如果上传成功
				// 获取光标所在位置
				let length = quill.getSelection().index;
				// 插入图片  res.info为服务器返回的图片地址
				quill.insertEmbed(length, 'image', data)
				// 调整光标到最后
				quill.setSelection(length + 1)
				// this.$message.error('图片插入失败')
				// loading动画消失
				this.quillUpdateImg = false
			},
			getInfo() {
				if (this.infoForm.id <= 0) {
					return false
				}
				//加载Product详情
				let that = this
				this.axios.get('goods/info', {
					params: {
						id: that.infoForm.id
					}
				}).then((response) => {
					let resInfo = response.data.data;
					let goodsInfo = resInfo.info;
					// goodsInfo.is_index = goodsInfo.is_index ? true : false;
					goodsInfo.is_new = goodsInfo.is_new ? true : false;
					goodsInfo.is_on_sale = goodsInfo.is_on_sale ? "1" : "0";
					that.infoForm = goodsInfo;
					that.kdValue = goodsInfo.freight_template_id;
					that.cateId = resInfo.category_id;
					that.getImgUrl();
				})
			},
			// 获取所有分类
			getAllCategory() {
				let that = this;
				this.axios.get('goods/getAllCategory', {
					params: {}
				}).then((response) => {
					that.options = response.data.data;
				})
			},
			getAllSpecification() {
				let that = this;
				this.axios.get('goods/getAllSpecification').then((response) => {
					let resInfo = response.data.data;
					console.log(resInfo);
					that.specOptionsList = resInfo;
				})
			},
			getExpressData() {
				let that = this
				this.axios.get('goods/getExpressData', {
					params: {}
				}).then((response) => {
					let options = response.data.data;
					that.kdOptions = options.kd;
					that.cateOptions = options.cate;
				})
			},
			// summernote 上传图片，返回链接
			sendFile(file) {},
			// 初始化 summernote
			initSummerNote() {
				let that = this;
				$('#summernote').summernote({
						lang: 'zh-CN',
						placeholder: 'Please Enter product Description',
						height: 300,
						minHeight: 300,
						maxHeight: 400,
						focus: true,
						callbacks: {
							onBlur: function(e) {
								console.log(" on blur ");
								console.log($('#summernote').summernote('code'));
								that.infoForm.goods_desc = $('#summernote').summernote('code');
							},
							onImageUpload: function(files) {
								console.log("onImageUpLoad...");
								that.sendFile(files[0]);
							}
						}
					}),
					// console.error(that.infoForm.goods_desc);
					$('#summernote').summernote('code', that.infoForm.goods_desc)
			},
		},
		components: {
			ElFormItem,
			ElForm,
			quillEditor,
			draggable
		},
		computed: {
			editor() {
				return this.$refs.myTextEditor.quillEditor
			}
		},
		mounted() {
			this.infoForm.id = this.$route.query.id || 0;
			this.getInfo();
			this.getAllCategory();
			this.getExpressData();
			this.getQiniuToken();
			this.getAllSpecification();
			if (this.infoForm.id > 0) {
				this.getSpecData();
				this.getGalleryList();
			}
			this.root = api.rootUrl;
			this.qiniuZone = api.qiniu;
		},
	}
</script>

<style scoped>
	.shadow,
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

	.gallery-item {
		display: flex;
		justify-content: center;
		align-items: center;
		float: left;
		position: relative;
	}

	.gallery-item:hover .shadow {
		opacity: 1;
	}

	.video-wrap {
		width: 300px;
	}

	.dialog-header {
		display: flex;
		justify-content: flex-start;
		margin-bottom: 10px;
	}

	.dialog-header .value {
		width: 150px;
		margin-right: 14px;
	}

	.input-wrap .el-input {
		width: 200px;
		float: left;
		margin: 0 20px 20px 0;
	}

	.input-wrap .el-input input {
		background-color: #fff !important;
		color: #233445 !important;
	}

	.specFormDialig .el-input {
		width: 150px;
		margin-right: 10px;
	}

	.el-select-class {
		width: 200px;
		margin-right: 20px;
	}

	.sepc-form {
		display: flex;
		justify-content: flex-start;
		margin-bottom: 10px;
	}

	.spec-form-wrap {
		margin-top: 0 !important;
	}

	.add-spec {
		margin-top: 10px;
	}

	.spec-form-wrap .header {
		display: flex;
		justify-content: flex-start;
	}

	.spec-form-wrap .header .l {
		width: 200px;
		margin-right: 20px;
	}

	.spec-form-wrap .header .m {
		width: 200px;
		margin-right: 20px;
	}

	.spec-form-wrap .header .m {
		width: 200px;
		margin-right: 20px;
	}

	/*.sepc-form div{*/
	/*margin-left: 0;*/
	/*}*/

	.float-right {
		float: right;
	}

	.sepc-form .el-input {
		width: 200px;
		margin-right: 20px;
	}

	.marginTop20 {
		margin-top: 20px;
	}

	.checkbox-wrap .checkbox-list {
		float: left;
		margin-right: 20px;
	}

	.upload_ad {
		display: none;
	}

	.upload_ad .el-upload--picture-card {
		display: none;
	}

	.ql-container {
		min-height: 200px;
		max-height: 400px;
		overflow-y: auto;
	}

	.image-uploader-diy {
		/*height: 200px;*/
		position: relative;
	}

	.image-uploader-diy .el-upload {
		border: 1px solid #d9d9d9;
		cursor: pointer;
		position: relative;
		overflow: hidden;
	}

	.image-uploader-diy .el-upload:hover {
		border-color: #20a0ff;
	}

	.image-uploader-diy .image-uploader-icon {
		font-size: 28px;
		color: #8c939d;
		width: 200px;
		height: 200px;
		line-height: 200px;
		text-align: center;
	}

	.image-uploader-diy .image-show {
		min-width: 148px;
		height: 148px;
		background-color: #f9f9f9;
		display: block;
	}

	.index-image {
		width: 148px;
		height: 148px;
		position: relative;
	}

	.index-image:hover .o-shadow {
		opacity: 1;
	}

	.image-uploader-diy .new-image-uploader {
		font-size: 28px;
		color: #8c939d;
		width: 165px;
		height: 105px;
		line-height: 105px;
		text-align: center;
	}

	.image-uploader-diy .new-image-uploader .image-uploader-icon {
		font-size: 28px;
		color: #8c939d;
		width: 165px;
		height: 105px;
		line-height: 105px;
		text-align: center;
	}

	.image-uploader-diy .new-image-uploader .image-show {
		width: 165px;
		height: 105px;
		display: block;
	}

	.item-url-image-fuzhu .el-input {
		width: 260px;
	}

	.hidden {
		display: none;
	}
</style>

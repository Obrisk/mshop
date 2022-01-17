<template>
	<div class="content-page">
		<div class="content-nav">
			<el-breadcrumb class="breadcrumb" separator="/">
				<el-breadcrumb-item>Ads List</el-breadcrumb-item>
			</el-breadcrumb>
			<div class="operation-nav">
				<router-link to="/dashboard/ad/add">
					<el-button type="primary" icon="plus">Add New Ads</el-button>
				</router-link>
			</div>
		</div>
		<div class="content-main">
			<div class="form-table-box">
				<el-table :data="tableData" style="width: 100%" border stripe>
					<el-table-column prop="id" label="ID" width="70px"></el-table-column>
                    <el-table-column prop="image_url" label="Ads">
                        <template scope="scope">
                            <img  :src="scope.row.image_url" alt="" style="width: 90px;height: 50px">
                        </template>
					</el-table-column>
					<el-table-column prop="goods_id" label="Product"></el-table-column>
					<el-table-column prop="end_time" label="End Date"></el-table-column>
					<el-table-column prop="sort_order" label="Sort" width="100" sortable>
						<template scope="scope">
							<el-input v-model="scope.row.sort_order" placeholder="Sort" @blur="submitSort(scope.$index, scope.row)"></el-input>
						</template>
					</el-table-column>
                    <el-table-column prop="enabled" label="Ad Switch" width="120px">
                        <template scope="scope">
                            {{ scope.row.enabled == 1 ? 'Turned On' : 'Disabled' }}
                        </template>
					</el-table-column>
					<el-table-column label="Switch" width="80">
						<template scope="scope">
							<el-switch
									v-model="scope.row.enabled"
									active-text=""
									inactive-text=""
									@change='changeStatus($event,scope.row.id)'>
							</el-switch>
						</template>
					</el-table-column>
					<el-table-column label="Action" width="170">
						<template scope="scope">
							<el-button size="small" @click="handleRowEdit(scope.$index, scope.row)">Edit</el-button>
							<el-button size="small" type="danger" @click="handleRowDelete(scope.$index, scope.row)">Delete</el-button>
						</template>
					</el-table-column>
				</el-table>
			</div>
			<div class="page-box">
				<el-pagination @current-change="handlePageChange" :current-page="page" :page-size="10" layout="total, prev, pager, next, jumper" :total="total">
				</el-pagination>
			</div>
		</div>
	</div>
</template>

<script>

export default {
	data() {
		return {
			page: 1,
			total: 0,
			filterForm: {
				name: ''
			},
			tableData: []
		}
	},
	methods: {
        test(){
            console.log(this.tableData);
		},
        submitSort(index, row){
            this.axios.post('ad/updateSort', { id: row.id,sort:row.sort_order }).then((response) => {
            })
        },
        changeStatus($event, para) {
            this.axios.get('ad/saleStatus', {
                params: {
                    status: $event,
                    id: para
                }
            }).then((response) => {

            })
        },
		handlePageChange(val) {
			this.page = val;
			//保存到localStorage
			localStorage.setItem('adPage', this.page)
			localStorage.setItem('adFilterForm', JSON.stringify(this.filterForm));
			this.getList()
		},
		handleRowEdit(index, row) {
			this.$router.push({ name: 'ad_add', query: { id: row.id } })
		},
		handleRowDelete(index, row) {

			this.$confirm('Are you sure you want to Delete?', 'Prompt', {
				confirmButtonText: 'Confirm',
				cancelButtonText: 'Cancel',
				type: 'warning'
			}).then(() => {

				this.axios.post('ad/destory', { id: row.id }).then((response) => {
					console.log(response.data)
					if (response.data.errno === 0) {
						this.$message({
							type: 'success',
							message: 'Deleted Successfully!'
						});

						this.getList();
					}
				})


			});
		},
		onSubmitFilter() {
			this.page = 1
			this.getList()
		},
		getList() {
			this.axios.get('ad', {
				params: {
					page: this.page,
				}
			}).then((response) => {
                this.tableData = response.data.data.data
                this.page = response.data.data.currentPage
                this.total = response.data.data.count
			})
			console.log(this.tableData);
		}
	},
	components: {

	},
	mounted() {
		this.getList();
	}
}

</script>

<style scoped>

</style>

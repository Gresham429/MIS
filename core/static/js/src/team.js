// 弹窗处理函数
function openPopup(teamId) {
    // 使用 jQuery 发送 AJAX 请求获取团队详细信息
    $.ajax({
        url: `/api/${teamId}/getPopUpContent/`,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // 构建弹窗内容
            var team_data = JSON.parse(data.team_data);
            var team_members_data = JSON.parse(data.team_members_data);
            var team = team_data[0];

            var PopUpContent = '';
            PopUpContent += '<p><strong>团队名称：</strong>' + (team.fields.name || '') + '</p>';
            PopUpContent += '<p><strong>团队信息：</strong>' + (team.fields.description || '') + '</p>';
            PopUpContent += '<hr>';

            PopUpContent += '<p><strong>团队成员</strong></p>';
            PopUpContent += '<hr>';
            team_members_data.forEach(function (member) {
                PopUpContent += '<p>姓名: ' + (member.fields.name || '') + '</p>';
                PopUpContent += '<button class="btn btn-primary btn-sm view-details" data-member-pk="' + member.pk + '">查看详细</button>';
                PopUpContent += '<hr>';
            });


            // 使用 Bootstrap 的 modal 创建弹窗
            $('#myModal .modal-body').html(PopUpContent); // 设置弹窗内容
            $('#myModal').modal('show'); // 显示弹窗
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}

$('#myModal .modal-body').on('click', '.view-details', function (event) {
    event.preventDefault();

    var member_id = $(this).data('member-pk');

    $.ajax({
        url: '/api/' + member_id + '/getMemberInfo/',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            var teamMemberData = JSON.parse(data.team_member);
            var teamMember = teamMemberData[0];
            $('#teamMemberModal #memberName').text(teamMember.fields.name);
            $('#teamMemberModal #memberMIBID').text(teamMember.fields.MIB_ID);
            $('#teamMemberModal #memberStudentID').text(teamMember.fields.student_id);
            $('#teamMemberModal #memberEmail').text(teamMember.fields.email);
            $('#teamMemberModal').modal('show');
        },
        error: function (error) {
            console.error('Error', error);
        },
    });
});


function fetchTeams() {
    // 使用 jQuery 发送 AJAX 请求获取团队信息
    $.ajax({
        url: '/api/get_teams_info/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var team_list = data;
            var team_container = $('#team-container');

            for (var i = 0; i < team_list.length; i++) {
                var team = team_list[i];
                var info = '<div class="col-lg-4 col-md-6">' +
                    '<div class="team-card">' +
                    '<h2>' + team.name + '</h2>' +
                    '<button type="button" class="btn btn-primary" onclick=\'openPopup("' + team.id + '")\'>查看详情</button>' +
                    '<button type="button" class="btn btn-danger delete-team-btn" data-team-id="' + team.id + '">删除团队</button>' +
                    '<button type="button" class="btn btn-warning edit-team-btn" data-team-id="' + team.id + '">编辑团队</button>' +
                    '</div>' +
                    '</div>';
                team_container.append(info);
            }

            // 设置删除按钮点击事件
            $('.delete-team-btn').click(function () {
                var teamId = $(this).data('team-id');
                $('#deleteConfirmModal').modal('show'); // 显示删除确认弹窗

                // 点击确认删除按钮时执行删除操作
                $('#confirmDeleteBtn').click(function () {
                    deleteTeam(teamId, csrftoken);
                    location.reload(); // 刷新整个页面
                });
            });

            // 编辑按钮点击事件
            $('.edit-team-btn').click(function () {
                var teamId = $(this).data('team-id');
                openEditModal(teamId, csrftoken);
            });
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}

// 处理新增团队
function handleAddTeam() {
    // 设置新增团队按钮点击事件
    $('#add-team-btn').click(function () {
        $('#add-team-form')[0].reset(); // 重置表单
        $('#add-team-error').hide(); // 隐藏错误消息
        $('#addTeamModal').modal('show'); // 显示新增团队弹窗
    });

    // 设置保存按钮点击事件
    $('#save-team-btn').click(function () {
        // 获取团队信息和logo文件
        var teamName = $('#team-name').val();
        var teamDescription = $('#team-description').val();
        var teamLogo = $('#team-logo')[0].files[0];

        // 创建 FormData 对象，用于发送 POST 请求
        var formData = new FormData();
        formData.append('name', teamName);
        formData.append('description', teamDescription);
        formData.append('logo', teamLogo);

        // 发送新增团队的 POST 请求
        $.ajax({
            url: '/api/add_team/',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (response) {
                $('#addTeamModal').modal('hide'); // 隐藏新增团队弹窗
                location.reload(); // 刷新页面以获取最新团队信息
            },
            error: function (xhr, textStatus, errorThrown) {
                if (xhr.status === 400) {
                    $('#add-team-error').text('团队名称已存在').show(); // 显示错误消息
                } else {
                    console.error('Error adding team:', textStatus, errorThrown);
                }
            }
        });
    });
}

// 处理新增团队成员
function handleAddTeamMember() {
    // 设置新增团队成员按钮点击事件
    $('#add-team-member-btn').click(function () {
        $('#add-team-member-form')[0].reset(); // 重置表单
        $('#add-team-member-error').hide(); // 隐藏错误消息
        $('#addTeamMemberModal').modal('show'); // 显示新增团队成员弹窗
    });

    // 设置保存按钮点击事件
    $('#save-team-member-btn').click(function () {
        // 获取团队成员信息

        var team_name = $('#teamname').val();
        var MIB_ID = $('#member-MIB-ID').val();
        var student_id = $('#member-student-id').val();
        var name = $('#member-name').val();
        var email = $('#member-email').val();

        // 创建发送的数据对象
        var postData = {
            team_name: team_name,
            MIB_ID: MIB_ID,
            student_id: student_id,
            name: name,
            email: email
        };

        // 发送新增团队成员的 POST 请求
        $.ajax({
            url: '/api/add_team_member/',
            method: 'POST',
            data: postData,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (response) {
                $('#addTeamMemberModal').modal('hide'); // 隐藏新增团队成员弹窗
                location.reload(); // 刷新页面以获取最新团队成员信息
            },
            error: function (xhr, textStatus, errorThrown) {
                if (xhr.status === 400) {
                    $('#add-team-member-error').text('找不到团队').show(); // 显示错误消息
                } else {
                    console.error('Error adding team member:', textStatus, errorThrown);
                }
            }
        });
    });
}

// 删除团队
function deleteTeam(teamId, csrftoken) {
    $.ajax({
        url: `/api/${teamId}/delete_team/`,
        method: 'DELETE',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
            // 处理删除成功后的操作，例如重新加载团队信息等
            $('#deleteConfirmModal').modal('hide'); // 隐藏删除确认弹窗
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log('Error deleting team:', textStatus, errorThrown);
            console.log('Delete button team ID:', teamId);
        }
    });
}

// 打开编辑弹窗
function openEditModal(teamId, csrftoken) {
    // 获取团队信息并填充到表格
    $.ajax({
        url: `/api/${teamId}/get_oneteam_info/`,
        method: 'GET',
        dataType: 'json',
        success: function (team) {
            $('#editModal #name').val(team.name);
            $('#editModal #description').val(team.description);
            $('#editModal').modal('show'); // 显示编辑弹窗

            getTeamMember(teamId, csrftoken);

            $('#saveEditBtn').click(function () {
                var editedTeam = {
                    name: $('#editModal #name').val(),
                    description: $('#editModal #description').val(),
                };
                saveEditedTeam(teamId, editedTeam, csrftoken);
            });
        },
        error: function (error) {
            console.error('Error fetching team info:', error);
        }
    });
}

function getTeamMember(teamId, csrftoken) {
    // 发送 AJAX 请求以获取团队成员数据
    $.get(`/api/${teamId}/get_team_members/`, function (data) {
        var members = data.team_members;
        var $memberList = $('#team-members-list'); // 成员列表容器

        // 清空成员列表
        $memberList.empty();

        // 遍历成员列表并将每位成员添加到列表中
        members.forEach(function (member) {
            var listItem = $('<div>').addClass('member-item');
            var deleteButton = $('<button>')
                .text('删除')
                .addClass('btn btn-danger btn-sm delete-member');
            var memberName = member.name;
            // 添加空格
            var space = document.createTextNode('  ');
            listItem.append(memberName, space, space, deleteButton);
            $memberList.append(listItem);

            // 为删除按钮添加点击事件
            deleteButton.on('click', function (event) {
                event.preventDefault();  // 阻止默认事件行为

                $('#deleteConfirmModal').modal('show');

                $('#confirmDeleteBtn').click(function () {
                    // 发送删除成员的请求，包括 CSRF 令牌
                    $.ajax({
                        url: '/api/' + member.id + '/delete_team_member/',
                        method: 'DELETE',
                        beforeSend: function (xhr) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        },
                        success: function (response) {
                            // 在成功回调中处理删除操作的响应
                            $('#deleteConfirmModal').modal('hide');
                            listItem.remove();
                            $('#editModal').modal('show'); // 显示编辑弹窗
                        },
                        error: function (xhr, textStatus, errorThrown) {
                            console.error('Error deleting team member:', textStatus, errorThrown);
                        }
                    });
                });
            });
        });
    });
}


// 保存编辑后的团队信息
function saveEditedTeam(teamId, editedTeam, csrftoken) {
    $.ajax({
        url: `/api/${teamId}/update_team/`,
        method: 'PUT',
        data: JSON.stringify(editedTeam), // 将数据转换为JSON格式
        contentType: 'application/json', // 指定请求数据类型为JSON
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (response) {
            $('#editModal').modal('hide'); // 隐藏编辑弹窗
            location.reload(); // 刷新页面以获取最新团队信息
        },
        error: function (error) {
            console.error('Error saving edited team:', error);
        }
    });
}

// 获取cookie中的CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
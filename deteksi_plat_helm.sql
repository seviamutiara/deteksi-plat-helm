
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 14, 2025 at 12:09 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `deteksi plat helm`
--

-- --------------------------------------------------------

--
-- Table structure for table `akun_kamera`
--

CREATE TABLE `akun_kamera` (
  `id` bigint(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `lokasi` varchar(200) NOT NULL,
  `status` varchar(10) NOT NULL,
  `waktu_ditambahkan` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `akun_kendaraan`
--

CREATE TABLE `akun_kendaraan` (
  `id_kendaraan` int(11) NOT NULL,
  `plat_nomor` varchar(15) NOT NULL,
  `jenis_kendaraan` varchar(50) NOT NULL,
  `foto_kendaraan` varchar(100) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `akun_notifikasi`
--

CREATE TABLE `akun_notifikasi` (
  `notif_id` int(11) NOT NULL,
  `status_baca` tinyint(1) NOT NULL,
  `metode` varchar(50) NOT NULL,
  `tanggal_kirim` datetime(6) NOT NULL,
  `admin_id` bigint(20) DEFAULT NULL,
  `pelanggaran_id` int(11) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `akun_pelanggaran`
--

CREATE TABLE `akun_pelanggaran` (
  `id_pelanggaran` int(11) NOT NULL,
  `waktu` datetime(6) NOT NULL,
  `lokasi` varchar(200) NOT NULL,
  `bukti_gambar` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `kendaraan_id` int(11) NOT NULL,
  `kamera_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `akun_user`
--

CREATE TABLE `akun_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `alamat` longtext DEFAULT NULL,
  `role` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `akun_user`
--

INSERT INTO `akun_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `no_hp`, `alamat`, `role`) VALUES
(4, 'pbkdf2_sha256$600000$z94YHctCOTia2eK2U9ujkD$OtxtFvbBICpGr4jAI2B2nK/PD+G1sa1CmKGI7JW8jOo=', '2025-06-14 09:35:50.537205', 1, 'vikraselpian', '', '', 'vikraselpian@gmail.com', 1, 1, '2025-06-11 12:48:54.121130', '085272343255', 'Laguna', 'admin'),
(7, 'pbkdf2_sha256$600000$QjECqL4TNLGLP3Vg0Gmlx2$FPaJKJanSPzIAyVh27P3b3PXpJ5L3jlwizpv/UEKdpE=', '2025-06-14 08:52:02.548308', 0, 'batam', '', '', 'batambatam2154@gmail.com', 0, 1, '2025-06-11 14:25:36.706721', '081266159139', 'Aviari', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `akun_user_groups`
--

CREATE TABLE `akun_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `akun_user_user_permissions`
--

CREATE TABLE `akun_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add kendaraan', 7, 'add_kendaraan'),
(26, 'Can change kendaraan', 7, 'change_kendaraan'),
(27, 'Can delete kendaraan', 7, 'delete_kendaraan'),
(28, 'Can view kendaraan', 7, 'view_kendaraan'),
(29, 'Can add pelanggaran', 8, 'add_pelanggaran'),
(30, 'Can change pelanggaran', 8, 'change_pelanggaran'),
(31, 'Can delete pelanggaran', 8, 'delete_pelanggaran'),
(32, 'Can view pelanggaran', 8, 'view_pelanggaran'),
(33, 'Can add notifikasi', 9, 'add_notifikasi'),
(34, 'Can change notifikasi', 9, 'change_notifikasi'),
(35, 'Can delete notifikasi', 9, 'delete_notifikasi'),
(36, 'Can view notifikasi', 9, 'view_notifikasi'),
(37, 'Can add kamera', 10, 'add_kamera'),
(38, 'Can change kamera', 10, 'change_kamera'),
(39, 'Can delete kamera', 10, 'delete_kamera'),
(40, 'Can view kamera', 10, 'view_kamera');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(10, 'akun', 'kamera'),
(7, 'akun', 'kendaraan'),
(9, 'akun', 'notifikasi'),
(8, 'akun', 'pelanggaran'),
(6, 'akun', 'user'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-06-07 03:15:49.747027'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-06-07 03:15:49.859678'),
(3, 'auth', '0001_initial', '2025-06-07 03:15:50.118609'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-06-07 03:15:50.178958'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-06-07 03:15:50.186429'),
(6, 'auth', '0004_alter_user_username_opts', '2025-06-07 03:15:50.197400'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-06-07 03:15:50.207419'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-06-07 03:15:50.213509'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-06-07 03:15:50.224328'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-06-07 03:15:50.233304'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-06-07 03:15:50.242925'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-06-07 03:15:50.257902'),
(13, 'auth', '0011_update_proxy_permissions', '2025-06-07 03:15:50.269891'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-06-07 03:15:50.280824'),
(15, 'akun', '0001_initial', '2025-06-07 03:15:51.060488'),
(16, 'admin', '0001_initial', '2025-06-07 03:15:51.239012'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-06-07 03:15:51.259957'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-07 03:15:51.280106'),
(19, 'sessions', '0001_initial', '2025-06-07 03:15:51.330768'),
(20, 'akun', '0002_alter_user_role', '2025-06-11 13:40:03.429523'),
(21, 'akun', '0003_alter_pelanggaran_status', '2025-06-14 08:45:16.694358'),
(22, 'akun', '0004_kamera', '2025-06-14 09:24:53.165830'),
(23, 'akun', '0005_pelanggaran_kamera', '2025-06-14 09:41:21.522342');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `akun_kamera`
--
ALTER TABLE `akun_kamera`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `akun_kendaraan`
--
ALTER TABLE `akun_kendaraan`
  ADD PRIMARY KEY (`id_kendaraan`),
  ADD KEY `akun_kendaraan_user_id_a87e69e6_fk_akun_user_id` (`user_id`);

--
-- Indexes for table `akun_notifikasi`
--
ALTER TABLE `akun_notifikasi`
  ADD PRIMARY KEY (`notif_id`),
  ADD KEY `akun_notifikasi_admin_id_89c72cb1_fk_akun_user_id` (`admin_id`),
  ADD KEY `akun_notifikasi_pelanggaran_id_d63fdd39_fk_akun_pela` (`pelanggaran_id`),
  ADD KEY `akun_notifikasi_user_id_4b466687_fk_akun_user_id` (`user_id`);

--
-- Indexes for table `akun_pelanggaran`
--
ALTER TABLE `akun_pelanggaran`
  ADD PRIMARY KEY (`id_pelanggaran`),
  ADD KEY `akun_pelanggaran_kendaraan_id_a017f71b_fk_akun_kend` (`kendaraan_id`),
  ADD KEY `akun_pelanggaran_kamera_id_6846760c_fk_akun_kamera_id` (`kamera_id`);

--
-- Indexes for table `akun_user`
--
ALTER TABLE `akun_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `akun_user_groups`
--
ALTER TABLE `akun_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `akun_user_groups_user_id_group_id_48e2c11b_uniq` (`user_id`,`group_id`),
  ADD KEY `akun_user_groups_group_id_fcb717dd_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `akun_user_user_permissions`
--
ALTER TABLE `akun_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `akun_user_user_permissions_user_id_permission_id_420c1e07_uniq` (`user_id`,`permission_id`),
  ADD KEY `akun_user_user_permi_permission_id_0b18c30f_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_akun_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `akun_kamera`
--
ALTER TABLE `akun_kamera`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `akun_kendaraan`
--
ALTER TABLE `akun_kendaraan`
  MODIFY `id_kendaraan` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `akun_notifikasi`
--
ALTER TABLE `akun_notifikasi`
  MODIFY `notif_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `akun_pelanggaran`
--
ALTER TABLE `akun_pelanggaran`
  MODIFY `id_pelanggaran` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `akun_user`
--
ALTER TABLE `akun_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `akun_user_groups`
--
ALTER TABLE `akun_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `akun_user_user_permissions`
--
ALTER TABLE `akun_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `akun_kendaraan`
--
ALTER TABLE `akun_kendaraan`
  ADD CONSTRAINT `akun_kendaraan_user_id_a87e69e6_fk_akun_user_id` FOREIGN KEY (`user_id`) REFERENCES `akun_user` (`id`);

--
-- Constraints for table `akun_notifikasi`
--
ALTER TABLE `akun_notifikasi`
  ADD CONSTRAINT `akun_notifikasi_admin_id_89c72cb1_fk_akun_user_id` FOREIGN KEY (`admin_id`) REFERENCES `akun_user` (`id`),
  ADD CONSTRAINT `akun_notifikasi_pelanggaran_id_d63fdd39_fk_akun_pela` FOREIGN KEY (`pelanggaran_id`) REFERENCES `akun_pelanggaran` (`id_pelanggaran`),
  ADD CONSTRAINT `akun_notifikasi_user_id_4b466687_fk_akun_user_id` FOREIGN KEY (`user_id`) REFERENCES `akun_user` (`id`);

--
-- Constraints for table `akun_pelanggaran`
--
ALTER TABLE `akun_pelanggaran`
  ADD CONSTRAINT `akun_pelanggaran_kamera_id_6846760c_fk_akun_kamera_id` FOREIGN KEY (`kamera_id`) REFERENCES `akun_kamera` (`id`),
  ADD CONSTRAINT `akun_pelanggaran_kendaraan_id_a017f71b_fk_akun_kend` FOREIGN KEY (`kendaraan_id`) REFERENCES `akun_kendaraan` (`id_kendaraan`);

--
-- Constraints for table `akun_user_groups`
--
ALTER TABLE `akun_user_groups`
  ADD CONSTRAINT `akun_user_groups_group_id_fcb717dd_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `akun_user_groups_user_id_de432874_fk_akun_user_id` FOREIGN KEY (`user_id`) REFERENCES `akun_user` (`id`);

--
-- Constraints for table `akun_user_user_permissions`
--
ALTER TABLE `akun_user_user_permissions`
  ADD CONSTRAINT `akun_user_user_permi_permission_id_0b18c30f_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `akun_user_user_permissions_user_id_d6b38c73_fk_akun_user_id` FOREIGN KEY (`user_id`) REFERENCES `akun_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_akun_user_id` FOREIGN KEY (`user_id`) REFERENCES `akun_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

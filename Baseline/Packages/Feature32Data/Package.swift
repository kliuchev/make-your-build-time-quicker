// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature32Data",
    products: [.library(name: "Feature32Data", targets: ["Feature32Data"])],
    dependencies: [.package(path: "../Feature32Domain")],
    targets: [.target(name: "Feature32Data", dependencies: [.product(name: "Feature32Domain", package: "Feature32Domain")])]
)

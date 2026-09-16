// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature31Data",
    products: [.library(name: "Feature31Data", targets: ["Feature31Data"])],
    dependencies: [.package(path: "../Feature31Domain")],
    targets: [.target(name: "Feature31Data", dependencies: [.product(name: "Feature31Domain", package: "Feature31Domain")])]
)

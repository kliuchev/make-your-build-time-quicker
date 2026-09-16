// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature27Data",
    products: [.library(name: "Feature27Data", targets: ["Feature27Data"])],
    dependencies: [.package(path: "../Feature27Domain")],
    targets: [.target(name: "Feature27Data", dependencies: [.product(name: "Feature27Domain", package: "Feature27Domain")])]
)

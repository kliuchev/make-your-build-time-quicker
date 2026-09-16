// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature06Data",
    products: [.library(name: "Feature06Data", targets: ["Feature06Data"])],
    dependencies: [.package(path: "../Feature06Domain")],
    targets: [.target(name: "Feature06Data", dependencies: [.product(name: "Feature06Domain", package: "Feature06Domain")])]
)

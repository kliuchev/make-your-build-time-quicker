// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature23Data",
    products: [.library(name: "Feature23Data", targets: ["Feature23Data"])],
    dependencies: [.package(path: "../Feature23Domain")],
    targets: [.target(name: "Feature23Data", dependencies: [.product(name: "Feature23Domain", package: "Feature23Domain")])]
)

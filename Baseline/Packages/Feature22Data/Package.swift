// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature22Data",
    products: [.library(name: "Feature22Data", targets: ["Feature22Data"])],
    dependencies: [.package(path: "../Feature22Domain")],
    targets: [.target(name: "Feature22Data", dependencies: [.product(name: "Feature22Domain", package: "Feature22Domain")])]
)

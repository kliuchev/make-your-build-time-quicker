// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature03Data",
    products: [.library(name: "Feature03Data", targets: ["Feature03Data"])],
    dependencies: [.package(path: "../Feature03Domain")],
    targets: [.target(name: "Feature03Data", dependencies: [.product(name: "Feature03Domain", package: "Feature03Domain")])]
)
